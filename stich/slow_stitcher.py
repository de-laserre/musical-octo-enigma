import cv2 as cv
import numpy as np
from collections import namedtuple


class SlowStitcher:
    def __init__(self, config):
        self.config = config

        if self.config.wave_correct == 'horiz':
            self.wave_correct = cv.detail.WAVE_CORRECT_HORIZ
        elif self.config.wave_correct == 'vert':
            self.wave_correct = cv.detail.WAVE_CORRECT_VERT
        else:
            self.wave_correct = None

        if self.config.features == 'orb':
            self.finder = cv.ORB.create()
        elif self.config.features == 'sift':
            self.finder = cv.SIFT_create()
        elif self.config.features == 'brisk':
            self.finder = cv.BRISK_create()
        else:
            self.finder = cv.AKAZE_create()

        if self.config.matcher == 'affine':
            self.matcher = cv.detail_AffineBestOf2NearestMatcher(False, self.config.cuda, self.config.match_conf)
        else:
            self.matcher = cv.detail_BestOf2NearestMatcher(self.config.cuda, self.config.match_conf)

        if self.config.estimator == 'affine':
            self.estimator = cv.detail_AffineBasedEstimator()
        else:
            self.estimator = cv.detail_HomographyBasedEstimator()

        if self.config.ba == 'ray':
            self.adjuster = cv.detail_BundleAdjusterRay()
        elif self.config.ba == 'reproj':
            self.adjuster = cv.cv.detail_BundleAdjusterReproj()
        elif self.config.ba == 'affine':
            self.adjuster = cv.cv.detail_BundleAdjusterAffinePartial()
        else:
            self.adjuster = cv.detail_NoBundleAdjuster()
        self.adjuster.setConfThresh(self.config.conf_thresh)
        refine_mask = np.zeros((3, 3), np.uint8)
        if self.config.ba_refine_mask[0] == 'x':
            refine_mask[0, 0] = 1
        if self.config.ba_refine_mask[1] == 'x':
            refine_mask[0, 1] = 1
        if self.config.ba_refine_mask[2] == 'x':
            refine_mask[0, 2] = 1
        if self.config.ba_refine_mask[3] == 'x':
            refine_mask[1, 1] = 1
        if self.config.ba_refine_mask[4] == 'x':
            refine_mask[1, 2] = 1
        self.adjuster.setRefinementMask(refine_mask)

        if self.config.expos_comp == 'gain_blocks':
            self.expos_comp = cv.detail.ExposureCompensator_GAIN_BLOCKS
            self.compensator = cv.detail.ExposureCompensator_createDefault(self.expos_comp)
        elif self.config.expos_comp == 'gain':
            self.expos_comp = cv.detail.ExposureCompensator_GAIN
            self.compensator = cv.detail.ExposureCompensator_createDefault(self.expos_comp)
        elif self.config.expos_comp == 'channel':
            self.expos_comp = cv.detail.ExposureCompensator_CHANNELS
            self.compensator = cv.detail_ChannelsCompensator(self.config.expos_comp_nr_feeds)
        elif self.config.expos_comp == 'channel_blocks':
            self.expos_comp = cv.detail.ExposureCompensator_CHANNELS_BLOCKS
            self.compensator = cv.detail_BlocksChannelsCompensator(
                self.expos_comp_block_size, self.expos_comp_block_size,
                self.expos_comp_nr_feeds)
        else:
            self.expos_comp = cv.detail.ExposureCompensator_NO
            self.compensator = cv.detail.ExposureCompensator_createDefault(self.expos_comp)

        if self.config.seam == 'dp_color':
            self.seam_finder = cv.detail_DpSeamFinder('COLOR')
        elif self.config.seam == 'dp_colorgrad':
            self.matcher = cv.detail_DpSeamFinder('COLOR_GRAD')
        elif self.config.seam == 'voronoi':
            self.matcher = cv.detail.SeamFinder_createDefault(cv.detail.SeamFinder_VORONOI_SEAM)
        else:
            cv.detail.SeamFinder_createDefault(cv.detail.SeamFinder_NO)


    def stitch_init(self, left_img_full, right_img_full):

        seam_work_aspect = 1
        full_img_sizes = [(left_img_full.shape[1], left_img_full.shape[0]),
                          (right_img_full.shape[1], right_img_full.shape[0])]

        if self.config.work_megapix < 0:
            left_img = left_img_full
            right_img = right_img_full
            work_scale = 1
        else:
            work_scale = min(1.0, np.sqrt(
                self.config.work_megapix * 1e6 / (left_img_full.shape[0] * left_img_full.shape[1])))
            left_img = cv.resize(src=left_img_full, dsize=None, fx=work_scale, fy=work_scale,
                                 interpolation=cv.INTER_LINEAR_EXACT)
            right_img = cv.resize(src=right_img_full, dsize=None, fx=work_scale, fy=work_scale,
                                  interpolation=cv.INTER_LINEAR_EXACT)

        if self.config.seam_megapix > 0:
            seam_scale = min(1.0, np.sqrt(
                self.config.seam_megapix * 1e6 / (left_img_full.shape[0] * left_img_full.shape[1])))
        else:
            seam_scale = 1.0

        seam_work_aspect = seam_scale / work_scale
        features = [
            cv.detail.computeImageFeatures2(self.finder, left_img),
            cv.detail.computeImageFeatures2(self.finder, right_img)
        ]

        left_img = cv.resize(src=left_img_full, dsize=None, fx=seam_scale, fy=seam_scale,
                             interpolation=cv.INTER_LINEAR_EXACT)
        right_img = cv.resize(src=right_img_full, dsize=None, fx=seam_scale, fy=seam_scale,
                              interpolation=cv.INTER_LINEAR_EXACT)
        images = [left_img, right_img]

        p = self.matcher.apply2(features)
        self.matcher.collectGarbage()

        # should be <class 'numpy.ndarray'>
        indices = [0, 1]

        b, cameras = self.estimator.apply(features, p, None)
        for cam in cameras:
            cam.R = cam.R.astype(np.float32)

        b, cameras = self.adjuster.apply(features, p, cameras)
        focals = []
        for cam in cameras:
            focals.append(cam.focal)
        focals.sort()
        warped_image_scale = (focals[len(focals) // 2] + focals[len(focals) // 2 - 1]) / 2

        if self.wave_correct is not None:
            rmats = []
            for cam in cameras:
                rmats.append(np.copy(cam.R))
            rmats = cv.detail.waveCorrect(rmats, self.wave_correct)
            for idx, cam in enumerate(cameras):
                cam.R = rmats[idx]

        corners = []
        masks_warped = []
        images_warped = []
        sizes = []
        masks = [cv.UMat(255 * np.ones((images[0].shape[0], images[0].shape[1]), np.uint8)),
                 cv.UMat(255 * np.ones((images[1].shape[0], images[1].shape[1]), np.uint8))]
        warper = cv.PyRotationWarper(self.config.warp, warped_image_scale * seam_work_aspect)

        K_left = cameras[0].K().astype(np.float32)
        swa = seam_work_aspect
        K_left[0, 0] *= swa
        K_left[0, 2] *= swa
        K_left[1, 1] *= swa
        K_left[1, 2] *= swa
        corner_left, image_wp_left = warper.warp(images[0], K_left, cameras[0].R, cv.INTER_LINEAR, cv.BORDER_REFLECT)
        corners.append(corner_left)
        sizes.append((image_wp_left.shape[1], image_wp_left.shape[0]))
        images_warped.append(image_wp_left)
        p_left, mask_wp_left = warper.warp(masks[0], K_left, cameras[0].R, cv.INTER_NEAREST, cv.BORDER_CONSTANT)
        masks_warped.append(mask_wp_left.get())

        K_right = cameras[1].K().astype(np.float32)
        K_right[0, 0] *= swa
        K_right[0, 2] *= swa
        K_right[1, 1] *= swa
        K_right[1, 2] *= swa
        corner_right, image_wp_right = warper.warp(images[1], K_right, cameras[1].R, cv.INTER_LINEAR, cv.BORDER_REFLECT)
        corners.append(corner_right)
        sizes.append((image_wp_right.shape[1], image_wp_right.shape[0]))
        images_warped.append(image_wp_right)
        p_right, mask_wp_right = warper.warp(masks[1], K_right, cameras[1].R, cv.INTER_NEAREST, cv.BORDER_CONSTANT)
        masks_warped.append(mask_wp_right.get())

        images_warped_f = []
        for img in images_warped:
            imgf = img.astype(np.float32)
            images_warped_f.append(imgf)

        self.compensator.feed(corners=corners, images=images_warped, masks=masks_warped)

        masks_warped = self.seam_finder.find(images_warped_f, corners, masks_warped)
        compose_scale = 1
        corners = []
        sizes = []
        blender = None

        # left
        compose_work_aspect = compose_scale / work_scale
        warped_image_scale *= compose_work_aspect
        warper = cv.PyRotationWarper(self.config.warp, warped_image_scale)

        # update
        cameras[0].focal *= compose_work_aspect
        cameras[0].ppx *= compose_work_aspect
        cameras[0].ppy *= compose_work_aspect
        sz = (int(round(full_img_sizes[0][0] * compose_scale)),
              int(round(full_img_sizes[0][1] * compose_scale)))
        K_left = cameras[0].K().astype(np.float32)
        roi = warper.warpRoi(sz, K_left, cameras[0].R)
        corners.append(roi[0:2])
        sizes.append(roi[2:4])
        cameras[1].focal *= compose_work_aspect
        cameras[1].ppx *= compose_work_aspect
        cameras[1].ppy *= compose_work_aspect
        sz = (int(round(full_img_sizes[1][0] * compose_scale)),
              int(round(full_img_sizes[1][1] * compose_scale)))
        K_right = cameras[1].K().astype(np.float32)
        roi = warper.warpRoi(sz, K_right, cameras[1].R)
        corners.append(roi[0:2])
        sizes.append(roi[2:4])
        
        # left
        _img_size = (left_img_full.shape[1], left_img_full.shape[0])
        K_left = cameras[0].K().astype(np.float32)
        print(cameras[1].R)
        corner_left, image_warped_left = warper.warp(left_img_full, K_left, cameras[0].R, cv.INTER_LINEAR, cv.BORDER_REFLECT)
        mask_left = 255 * np.ones((left_img_full.shape[0], left_img_full.shape[1]), np.uint8)
        p, mask_warped_left = warper.warp(mask_left, K_left, cameras[0].R, cv.INTER_NEAREST, cv.BORDER_CONSTANT)
        self.compensator.apply(0, corners[0], image_warped_left, mask_warped_left)
        image_warped_s_left = image_warped_left.astype(np.int16)
        dilated_mask_left = cv.dilate(masks_warped[0], None)
        seam_mask_left = cv.resize(dilated_mask_left, (mask_warped_left.shape[1], mask_warped_left.shape[0]), 0, 0, cv.INTER_LINEAR_EXACT)
        mask_warped_left = cv.bitwise_and(seam_mask_left, mask_warped_left)

        # blender init
        blender = cv.detail.Blender_createDefault(cv.detail.Blender_NO)
        dst_sz = cv.detail.resultRoi(corners=corners, sizes=sizes)
        blend_width = np.sqrt(dst_sz[2] * dst_sz[3]) * self.config.blend_strength / 100
        if blend_width < 1:
            blender = cv.detail.Blender_createDefault(cv.detail.Blender_NO)
        elif self.config.blend == "multiband":
            blender = cv.detail_MultiBandBlender()
            blender.setNumBands((np.log(blend_width) / np.log(2.) - 1.).astype(np.int32))
        elif self.config.blend == "feather":
            blender = cv.detail_FeatherBlender()
            blender.setSharpness(1. / blend_width)
        blender.prepare(dst_sz)

        blender.feed(cv.UMat(image_warped_s_left), mask_warped_left, corners[0])

        # right
        _img_size = (right_img_full.shape[1], right_img_full.shape[0])
        K_right = cameras[1].K().astype(np.float32)
        corner_right, image_warped_right = warper.warp(right_img_full, K_right, cameras[1].R, cv.INTER_LINEAR, cv.BORDER_REFLECT)
        mask_right = 255 * np.ones((right_img_full.shape[0], right_img_full.shape[1]), np.uint8)
        p, mask_warped_right = warper.warp(mask_right, K_right, cameras[1].R, cv.INTER_NEAREST, cv.BORDER_CONSTANT)
        self.compensator.apply(1, corners[1], image_warped_right, mask_warped_right)
        image_warped_s_right = image_warped_right.astype(np.int16)
        dilated_mask_right = cv.dilate(masks_warped[1], None)
        seam_mask_right = cv.resize(dilated_mask_right, (mask_warped_right.shape[1], mask_warped_right.shape[0]), 0, 0, cv.INTER_LINEAR_EXACT)
        mask_warped_right = cv.bitwise_and(seam_mask_right, mask_warped_right)
        blender.feed(cv.UMat(image_warped_s_right), mask_warped_right, corners[1])

        result = None
        result_mask = None
        result, result_mask = blender.blend(result, result_mask)
        zoom_x = 600.0 / result.shape[1]
        dst = cv.normalize(src=result, dst=None, alpha=255., norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
        dst = cv.resize(dst, dsize=None, fx=zoom_x, fy=zoom_x)
        cv.imshow('res', dst)
        cv.waitKey()

        print("Done")



if __name__ == '__main__':
    Config = namedtuple('Config',
                        [
                            'cuda',
                            'work_megapix',
                            'features',
                            'matcher',
                            'estimator',
                            'match_conf',
                            'conf_thresh',
                            'ba',
                            'ba_refine_mask',
                            'wave_correct',
                            'warp',
                            'seam_megapix',
                            'seam',
                            'expos_comp',
                            'expos_comp_nr_feeds',
                            'expos_comp_nr_filtering',
                            'expos_comp_block_size',
                            'blend',
                            'blend_strength',
                        ]
                        )
    config = Config._make(
        [
            False,
            0.6,
            'orb',
            'homography',
            'homography',
            0.3,
            1.0,
            'ray',
            'xxxxx',
            'horiz',
            'spherical',
            0.1,
            'dp_color',
            'gain_blocks',
            1,
            2,
            32,
            'multiband',
            5
        ]
    )

    left_img = cv.imread('./left.jpg')
    right_img = cv.imread('./right.jpg')

    slow_stitcher = SlowStitcher(config)
    slow_stitcher.stitch_init(left_img, right_img)
