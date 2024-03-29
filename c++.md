## black CPP

### C1 

#### helloworld

```c++
#include<iostream>
using namespace std;

int main()
{
	// 单行注释
	/*
		main是一个程序的入口，有且只能有一个main
	*/
	cout << "hello world" << endl;
	system("pause");
	return 0;
}
```

#### 变量

给一段内存空间命名，变量创建的语法： 数据类型 变量名 = 变量初始值

#### 常量

用于记录程序中不可更改的程序：1. #define 宏`#define Day 7`；2. const 修饰的变量

#### 关键字、标识符

标识符不能是关键字，只能由于字母数字下划线组成，第一个必须是字母或者下划线，区分大小写

#### 数据类型

存在的意义：给变量分配合适的内存空间

sizeof关键字可以统计hi数据类型占用的内存空间大小

整型：short 2字节；int 4 字节; 《= long; 《= long long； 

实型、浮点型：float 4字节；double 8 字节；

字符型：`char ch = 'a';` 一个字节；不是把字符存在内存中，而是把ascll存在内存中 a-97 A-65

转义字符：用于表示不能显示的ascll字符 \n \\\\ \t

字符串型：c风格字符串 `char str[] = ”asdf“ · const char * = ”asdf“`; C++风格字符串`string str= “helloworld”` (需要包含头文件 #include<string\>)

布尔类型：`bool flag = true` 占用一个字节; 非0值都代表真

数据的输入： cin >> a;

#### 运算符号

算数运算：+-*/ 舍去小数位; % ；++a（先让+1，在进行表达式运算）；--a；a++（先表达式，再加）; a--;

赋值运算：= += -= %= /=

比较运算：==   ！=  >=  <= > <

逻辑运算：! ; &&; ||

#### 程序流程

if

```c++
#include<iostream>
using namespace std;

int main()
{
	if (true)
	{
		if (true)
		{
			cout << "ifif";
		}
		cout << "if";
	}
	else if (true)
	{
		cout << "else if";
	}
	else
	{
		cout << "else";
	}
	system("pause");
	return 0;
}
```

三目运算符：表达式？a:b; 

`c = (a>b?a:b)`  三目返回的是变量，可以继续赋值`(a>b?a:b) = 100` 

swich

```C++
	int a = 0;
	switch (a)
	{
	case 1:
		break;
	case 2:
		break;
	default:
		break;
	}
```

while;for;do

```C++
	int a = 0;
	// while
	while (a < 10)
	{
		cout << a << endl;
	}
	// do while, 会先执行一次
	do
	{
		cout << a << endl;
	} while (a < 20);

	// for
	for (int i = 0; i < a; i++)
	{
		if (i == 6)
		{
			continue;
		}
		cout << a << endl;
	}
```

### C2 数组

放在一块连续的内存空间中，每个元素都是相同的数据类型，定义数组时候必须知道元素个数

定义方法：int score[10]; int score[2] = {2，3}； int score[] = {2，3}

sizeof(score) /sizeof(score[0])数组长度；score 表示数组的首地址，第一个元素地址；

int arr \[2][3]; int arr \[2][2] = {{1,2},{3,4}}; int arr \[2][2] = {1,2,3,4}; int arr \[][2] = {1,2,3,4}; 

### C3 函数

返回值类型；函数名；参数列表； 函数体；return；

参数列表的的是形参，调用的时候实参的值会传递给形参；形参数发生改变不会影响实参

无参无返；有参无返；无参有返；有参有返；

函数声明：提前告诉编译器函数的存在；没有函数体；函数定义在main函数之后

函数的分文件编写：

创建.h头文件；创建.cpp源文件；有文件中写函数声明；源文件（#include “swap.h”）写函数定义；

函数的参数允许有默认值，有默认值的参数必须写在没有默认值的参数之后

如果函数声明有默认值，实现就不能有默认参数了，不能重定义默认参数

函数占位参数：参数列表中只填数据类型，调用的时候必须传

函数重载：同一个作用域，函数名称相同，参数类型不同，个数不同或顺序不同（返回值不同不行）

引用作为函数重载条件：

函数重载默认参数坑点：调用函数不知道应该选择哪一个也会报错

```C++
void func(int& a)
{
	cout << "int& a" << endl;
}
void func(const int& a)
{
	cout << "const int& a" << endl;
}

void func(int a)
{
	cout << "int& a" << endl;
}
// 保存
void func(int a, int b = 10)
{
	cout << "const int& a" << endl;
}

int main()
{
	int a = 10;
	func(a); // 第一个
	func(10); // 第二个

	system("pause");
	return 0;
}
```



### C4 指针

可以通过指针间接访问内存, 定义指针通过取地址符为指针赋值，在指针前使用取地址获取指针值

指针是数据类型，是地址，在32位中4个字节，64位8个字节

空指针：指针变量指向内存中编号为0d的空间，是不可访问的，用于给指针变量初始化 `int * p = Null`

野指针：int * p = (int *) 0x0100; 没有权利操作

#### const 修饰指针

const修饰指针，常量指针 const int * p = &a; 指针指向可以修改，但不能通过指针修改指向的值，静态遥控器

const修饰常量，指针常量  int * const p = &a; 指针本身不可以改，指向不可以改，值可以改

const修饰常量也修饰指针 const int * const p = &a； 都不可以改

#### 指针和数组

int * p = arr;  p++(指针偏移4个字节，访问数组元素)

#### 指针和函数

参数是指针传入，可以修改值并改变实参

### C5 结构体

用户自定义的数据类型，可以存储不同的数据类型

（sturct可以省略，定义时不可以省略）student s1;  ；student s2 = { "happy", 10 };

结构体数组 student stuArr[3];

结构体指针 student* stuP = &s1; 通过指针访问结构体成员 stuP->age = 90; 

结构体做函数参数：值传递（不能修改实参），地址传递（可以修改）

#### 结构体中const使用场景

void printStudent(const student *s) 传入地址时防止通过指针修改元素

```c++
int main()
{
	student	s1;
	s1.name = "sad";
	s1.age = 10;
	student s2 = { "happy", 10 };

	student stuArr[2];

	student* stuP = &s1;
	stuP->age = 90;


	system("pause");
	return 0;
}
```

### C6 

#### 程序内存模型

代码区：二进制代码，操作系统管理，程序运行前：存放cpu执行的机器指令，共享（内存中只需要一份）只读

全局区：全局、静态常量、全局静态常量

栈：编译器自动分配释放，函数参数，局部变量，形参；不要返回局部变量地址

堆：用户分配释放，程序结束回收，

利用new可以把数据放在堆区 int * p = new int(10); new 数据类型返回的是指针, delete p 释放内存

可以在函数内创建堆空间数组，int * arr = new int [10];  delete[] arr;

#### 引用

内存空间的别名：int a = 10; int &b = a;  引用必须初始化， 初始化后不可再更改

引用作为函数参数：可以修改实参的值，引用传递，相当于用形参给实参起了别名

引用作为函数返回值：不要返回局部变量的引用，int& fnc(){}  ,函数的返回值是引用，可以作为左值赋值

引用的本质：内部实现是指针常量 int& red = a ; int * const red = &a; func(int& ref) ref是指针 ref= 1 自动转换位 *ref = 20

常量引用：主要用来修饰形参，防止误操作； print（const & val）

int a = 10; int & ref = 10(错，引用必须引用一块合法的空间) const int & ref = 10, ref 变为只读；

### STL

 standard Template Library 标准模板库：广义分为 容器 算法 迭代器，容器和算法通过迭代器进行连接

六大组件：容器，算法迭代器，仿函数，适配器，空间配置器

容器：各种数据结构，vector、list，map，将最广发使用的数据结构实现

​	序列式容器：固定位置； 关联式容器，二叉树结构，没有严格顺序

算法：find copy foreach sort，质变算法：改变值，非质变算法：不会改变

迭代器：提供一种方法，使得能够按照顺序方位容器中的元素，双向迭代器，随机访问迭代器（只读，只写，前向）

仿函数：行为类似函数，作为算法的某种策略

#### vector

算法：for_each; 迭代器 vector\<int> ::iterator, 迭代器看作指针

```C++
#include<string>
#include<iostream>
#include<vector>;
#include<algorithm>

using namespace std;

void myPrintFunc()
{

}

int main()
{

	vector<int> v;
	v.push_back(10);
	vector<int>::iterator itBegin= v.begin();
	vector<int>::iterator itEnd = v.end();//最后一个元素的下一个
	// vector 遍历
	while (itBegin != itEnd)
	{
		itBegin++;
	}

	for (vector<int>::iterator it = v.begin(); it != v.end(); it++)
	{
        // (*it)就是《中的东西》
		cout << (*it).name << endl;
		cout << it->name << endl;
		// 如果迭代器存的地址
		cout << (*it)->name << endl;
		cout << (**it).name << endl;
	}

	for_each(v.begin(), v.end(), myPrintFunc);



	system("pause");
	return 0;
}
```

vector是动态扩展：找更大空间，把元数据拷到新空间，支持随机访问的迭代器

构造函数：

​	vector\<T> v; // 模板类实现， 默认构造函数

​	vector(v.begin(), v.end()) //前闭后开区间拷贝

​	vector(n, element) // 拷贝n个ele

​	vector(const vector &vec) // 拷贝构造函数

```C++
int main()
{
	/*vector 赋值*/
	vector<int> v1;
	vector<int> v2;
	v2 = v1;
	v2.assign(v1.begin(), v1.end());
	v2.assign(1, 100);

	/*size*/
	v1.empty();
	v1.capacity();
	v1.size();

	v1.resize(int num, elem);//重新变换长度，若更长可以以默认值或ele填充，变短删尾

	/*插入删除*/
	v1.push_back(1);
	v1.pop();
	v1.insert(const_iteraor, ele);//在迭代器位置pos插入元素
	v1.insert(const_iteraor,n, ele);//在迭代器位置pos插入n个元素
	v1.erase(const_iteraor); //
	v1.erase(const_iteraor, const_enditeraor); //删除之间
	v1.clear();

	/*存取*/
	v1.at(idx);
	v1[0];
	v1.front();//第一个元素
	v1.back();//最后一个

	/*互换*/
	v1.swap(v2);
	vector<int>(v1).swap(v1);// 巧用呼唤收缩内存

	/*预留空间*/
	v1.reserve(int len)// 减少扩张次数

	system("pause");
	return 0;
}
```



#### string

本质是一个类，内部封装了char\*(c 风格字符串)，是一个char\*型的容器，内部封装了很多成员方法find copy...

管理char\* 所分配的内存 不用担心赋值越界，取值越界问题，用内部负责

构造函数：

​	string（）；//

​	string（const char* s）；//使用c风格字符串

​	string（const string& str）；拷贝构造

​	string（int a , char c）；n个c构造

```C++
int main()
{

	/*赋值方法*/
	string str;
	string str1 = "";
	str = "hello";// string& operator=(const char* s)
	str = str1;// string& operator=(const string &s)
	str = 'c';// string& operator=(char c)
	str.assign("hello");// string& assign(const char *s)
	str.assign("hello", 3);// string& assign(const char *s, int n),前3个
	str.assign("hello");// string& assign(const string &s),前3个
	str.assign(5, 'c');// string& assign(int n, char c),前3个

	/*拼接操作*/
	//重载+=，char *;string char
	//append,...
	str.append("hellopp", 0, 2);//从0开始截取两个

	/*查找替换*/
	str.find("字符或字符串");// int find(const string & s, int pos = 0) const;
	str.find("字符或字符串", 0, int n);//从pos起，前n个字符第一次出现位置
	str.rfind("s"); // 最后一次出现位置

	str.replace(int pos, int n, const char* s);// 从pos开始的n个字符替换位s

	/*字符窜比较*/
	string str2 = "hello";
	string str3 = "hello22";
	str2.compare(str3) == 0;//首字母的ascll码比较，用于比较相等，相等逐个对比

	/*单个字符存取,读或写都可以*/
	str2[0];//char& operator[](int n);
	str2.at(0);//char& at(int n);

	/*插入或者删除*/
	
	str1.insert(0, "");// string& insert(int pos, const char * s)
	str1.insert(0, 3,'c');//0 开始插入3个c
	str1.erase(0, 5);//删除从0开始的n个字符
	
	/*子窜*/
	str1.substr(0, str1.find("@"))// string subStr(int pos, int n);从pos开始截取n个

	system("pause");
	return 0;
}
```

	#### deque

vector头插需要移动版元素，访问比deque快，连续线性空间内；

deque内部有中控器，维护每个缓存区的内容，缓存区存真实数据，是的deque像一片连续的内存空间

push_back; push_front;pop_back;pop_front;

```c++
void myPrintFunc(const deque<int>& d)
{
	for (deque<int>::const_iterator i = d.begin(); i != d.end(); i++)
	{

	}

```

#### stack

没有遍历i行为 

stack\<T> stk; //默认构造

stack(const stack &stk) //拷贝构造

重载等号赋值

push();pop();top()  empty(); size()

#### queue

没有遍历i行为 

queue\<T> queue; //默认构造

queue(const queue&q) //拷贝构造

重载等号赋值

push();pop();back();front(); empty(); size()

#### set multiset

所有元素都会在插入的时候排序，关联式容器底层二叉树实现

set不允许重复元素， multiset 允许重复

构造：

set<T> st; set(const set &st); 默认构造拷贝构造

赋值 =

插入 insert ，支持迭代器遍历； erase（iter）erase(iter_begin, iter_end); erase(elem)

size() empty() swap() 不支持resize(因为填充默认值)

find() 若成功返回元素迭代器，否则返回set.end()  count()计数，对于set只能为1，0，

pair<set\<int>::iterator, bool> = s.insert(10); 插入返回位置迭代器和插入成功与否set，multiset只返回位置

自定义排序规则

```C++
class MyCompare {
public:
	bool operator()(int v1, int v2)const {
		return v1 > v2;
	}
};

class MyCompare {
public:
	bool operator()(const MyClass& v1, const MyClass& v2)const {
		return v1.age > v2.age;
	}
};


int main()
{
	set<int, MyCompare> s2;
	s2.insert(1);
	s2.insert(2);
	s2.insert(4);


	system("pause");
	return 0;
}

```

#### pair

成对出现的数据

pair<T1,T2> p(a,2); // 默认构造 pair<T1,T2> p = make_pair(1,2);, p.first p.second

#### map multimap

所有元素都是pair, key， value,  二叉树实现，根据key自动排序

默认构造 拷贝构造 =赋值

m.insert(pair(pair<int, int>(4,20)));  clear erase clear erase（按照key删除）

size empty swap

插入

m.insert(pair(pair<int, int>(4,20)));  m.insert(make_pair(11,22));  m[4] = 40;  m[] 每运行一次如果没有key会自动创建默认值

find()  count 统计key的元素个数

#### list

链式存储 一个存当前数据一个存下一个节点指针，双向链表

动态存储分配，不会造成浪费溢出，但是空间遍历耗费大，插入删除修改指针即可，不需要移动元素，插入删除list迭代器不会失效， vector不成立

默认构造 拷贝构造， list(n, ele) list(beg, end)

赋值 assign(n, ele); assign(beg, end) = swap

size empty resize() resize(n, ele);  

插入删除

pop_back pushback push front, insert(iter, ele)  insert(iter, n, ele)  insert(iter, beg, end)

remove(ele) ,删除值一样的所有数据

front() back() 返回第一个和最后一个元素

reverse（） sort()  li.reverse();  li.sort(mycompare函数bool)

### Object

C++ 面向对象的三大特性：封装（将属性和行为作为一个整体， 加以权限控制）继承多态

protected private（儿子不能访问）类外不可以访问

class默认访问权限是private struct默认public

构造函数：创建对象的时候给对象的成员属性赋值，编译器自动调用， 语法`类名(){}`

没有返回值不写void，函数名称与类名相同，可以有参数所有可以发生重载，调用时候自动调用，一次

析构函数：对象销毁前系统自动调用`~类名(){}` 不可重载 销毁时候自动调用，一次

编译器提供的构造函数和解析构函数是空实现

有参构造、无参数构造； 普通构造、拷贝构造

三种调用方法：括号 Person p（不能加括号，加括号编译器 识别为函数声明）; Person p(10); Person p(p1)  

显式法 Person p = Person(10)（y）、 Person p = Person(p2)；  Person(10)(匿名对象，马上被销毁)

Person（p1） -- 编译器识别为 Person p1 ,可能重定义，不要用通过拷贝构造创建匿名对象

拷贝构造函数调用时机：使用一个已经创建完的对象初始化新对象，值传递，以值方式返回局部对象

编译器自动 默认添加默认构造默认西构函数默认拷贝构造

如果用户定义有参构造，则不再提供默认无参，有拷贝

如果写了拷贝，就不会提供其他构造

浅拷贝：简单的赋值拷贝（内存重复释放）  深拷贝：在堆区重新申请空间，进行拷贝 mH=new int(*p.mH)

初始化列表 构造函数（）属性1（值），属性2（值）{}

```C++
Person(int a, int b, int c):m_A(a),m_B(b),m_C(c){

}
Person():m_A(1),m_B(2),m_C(4){

}
```

类对象作为类成员：构造顺序和析构函数相反

静态成员变量：所有对象共享同一份数据；在编译阶段分配内存；类内声明，类外初始化 全局区

可以通过对象访问，也可以通过类名访问  静态也有访问权限，private类外访问不到

```C++
class Per {
public:
	static int m_A;
};
int Per::m_A = 10;
int main()
{
	Per p;
	p.m_A = 100
    int a = Per::m_A;
	system("pause");
	return 0;
}
```

静态成员函数：所有对象共享一个函数，静态成员函数只能访问静态成员变量

通过对象访问，通过类名访问，也是有访问权限的

C++对象模型：成员变量和成员函数分开存储，，C++会给空对象分配一个字节空姐，为了区分空对象内存位置

只有非静态成员变量属于对象上 有一个int占用4个字节，非静态成员函数也不再类的对象上

this指针（指针常量，指向不可改）（解决名称冲突，区分用哪个对象的属性，解决参数与属性重名）：指向被调用的成员函数所属的对象，隐含在每一个非静态成员函数的内部

*this 对象 this->age 访问属性

this返回本体

```C++
class Per {
public:
	static int m_A;
	Per& add(Per& p) {
		return *this;
	}
};
```

防止空指针调用成员函数

if（this== nullptr）{return;}

const修饰成员函数

常函数：成员函数后加const（相当于const this），常函数不能修改成员属性，成员属性声明加关键字mutable,在常函数\常对象就可以修改了

常对象：对象前加const，常对象只能调用常函数

友元：friend 有些私有属性也想让类外函数方位

全局函数做友元；类做友元；成员函数做友元

```C++
class Per {
	//全局函数做友元
	friend void vistied(const Per& p);
	//类友元
	friend class Mycompare;
	//成员函数做友元
	friend bool MyCompare::isValid();
public:
	static int m_A;
	Per& add(Per& p) {
		return *this;
	}
private:
	string building;
};
```

运算符重载：

对已有的运算符号重新定义，赋予其另外一种功

通过成员函数重载加号

Class operator+(class &p2)

通过全局函数重载

Person operator+ （person &  p1, Person& p2）

重载<< 通常只能通过全局函数， ostream& operator<<(ostream & cout, Person p)

成元函数重载变成p << cout

赋值运算符重载 C++至少给一个类添加4个函数：默认构造默认析构默认拷贝构造 默认赋值运算

new出来的控件需要手动释放

Person& operator=(Person &p){

首先判断是否有属性在堆区，如果有先释放干净，再深拷贝，再返回自生引用

}	

（）函数调用运算符号重载，仿函数

void operator(){}

匿名函数对象 Myadd（）(100,100)

#### 继承

利用继承的特点减少重复代码

class Java ： public BasePage   class 子类 ： 继承方式 父类

继承方式 公共继承（除开private均可访问） 保护继承（除private ,其他都变成protected） 私有继承

（除private ,其他都变成private）

继承的对象模型：父类中所有的非静态成员属性都会子类继承，私有的被编译器隐藏，但是确实被继承下来了。

构造和析构顺序：先构造父类，再构造子类，析构先子类后父类

继承中同名的处理方式：

访问子类中同名成员 直接访问 p.name; 访问父类中同名成员 需要加作用域 p.Base::name

如果子类中出现和父类同名的成员函数，子类的同名成员会影藏掉父类所有的（包括重载）同名成员函数，如果需要访问需要加作用域

同名静态成员处理

访问子类同名，直接访问 访问父类同名，需要加作用域

多继承语法  class:继承方式 父类1， 继承方式 父类2

菱形继承：利用虚继承解决，再继承方式之前加长virtual关键词，数据就只有一份，继承两份指针，而不是两份数据， 会根据指针去找到同一份数据

 #### 继承

静态多态：函数重载，运算符重载复用函数名, 函数地址早绑定，编译阶段确定函数地址

动态多态： 派生类和虚函数实现运行时多态，运行阶段确定函数地址

动态多态：需要有继承关系，子类需要重写父类的虚函数；重写（返回，函数，参数列表完全相同）

子类覆盖的函数的virtual 可写可不写

动态多态使用：父类的指针或者引用，执行子类对象

```C++
class Animal {
public:
	void speak() {
		cout << "animal" << endl;
	}
};

class Cat : public Animal{
public:
	void speak() {
		cout << "cat" << endl;
	}
};

void speak(Animal& animal) {
	animal.speak();
}


int main()
{
	Cat c;
	c.speak();
	c.Animal::speak();
	speak(c);//animal
	//如果想让猫说话，那这个函数地址就不能提前绑定需要在运行阶段绑定
	// 如果 在Animal前加virtual 关键字 ，让起

	system("pause");
	return 0;
}
```

动态的原理：

增加vitual，class占用增加4字节的指针

虚函数 虚函数表指针 指向 虚 函数表 ，虚函数表记录虚函数地址：当子类重写覆盖父类虚函数，子类中的虚函数表地址会替换为子类的虚函数地址，当父类的指针指向子类对象时候，发生多态，

纯虚函数：vitual 返回值类型 函数名 (参数列表) = 0；

当类中存在纯虚函数，就是抽象类，不能实例化对象，子类必须重写抽象类中的纯虚函数，否则也属于抽象类。



多态使用中，如果子类属性开辟到堆区，那么父类指针在释放时无法调用到子类的析构代码，

解决方法：将析构改为虚析构

虚析构和纯虚析构：可以解决父类指针释放子类对象，都需要有具体的函数实现

如果是纯虚析构，则也是抽象类，无法实例化对象

virtual ~类名（）  纯虚析构  virtual ~类名（）  = 0
