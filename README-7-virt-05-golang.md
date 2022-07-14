# Домашнее задание к занятию "7.5. Основы golang"

С `golang` в рамках курса, мы будем работать не много, поэтому можно использовать любой IDE. 
Но рекомендуем ознакомиться с [GoLand](https://www.jetbrains.com/ru-ru/go/).  

## Задача 1. Установите golang.
1. Воспользуйтесь инструкций с официального сайта: [https://golang.org/](https://golang.org/).
2. Так же для тестирования кода можно использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

```bash
root@dev1-10:~# go version
go version go1.18.3 linux/amd64
```

## Задача 2. Знакомство с gotour.
У Golang есть обучающая интерактивная консоль [https://tour.golang.org/](https://tour.golang.org/). 
Рекомендуется изучить максимальное количество примеров. В консоли уже написан необходимый код, 
осталось только с ним ознакомиться и поэкспериментировать как написано в инструкции в левой части экрана.  

## Задача 3. Написание кода. 
Цель этого задания закрепить знания о базовом синтаксисе языка. Можно использовать редактор кода 
на своем компьютере, либо использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные 
у пользователя, а можно статически задать в коде.
    Для взаимодействия с пользователем можно использовать функцию `Scanf`:
    ```
    package main
    
    import "fmt"
    
    func main() {
        fmt.Print("Enter a number: ")
        var input float64
        fmt.Scanf("%f", &input)
    
        output := input * 2
    
        fmt.Println(output)    
    }
    ```

```bash

root@dev1-10:~/netol_do/go# go run test.go 
Please, enter meters: 10
10.000000 meters equals 32.808399 feets!
root@dev1-10:~/netol_do/go# cat test.go 
package main

import "fmt"

func main() {
        fmt.Print("Please, enter meters: ")
        var input float64
        fmt.Scanf("%f", &input)

        output := input / 0.3048

        fmt.Println(fmt.Sprintf("%f", input) + " meters equals " + fmt.Sprintf("%f", output) + " feets!")
}
root@dev1-10:~/netol_do/go# 

```

```shell

C:\Users\demi\Downloads>m-to-ft_windows_amd64.exe
Please, enter meters: 10
10.000000 meters equals 32.808399 feets!

C:\Users\demi\Downloads>

```

1. Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
    ```
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
    ```

```bash
root@dev1-10:~/netol_do/go# go run most-less.go 
Please, input digits one by one divided by space (lets try to find the smallest one): 223 3454 56 7676
The smallest one is:  56
root@dev1-10:~/netol_do/go# cat most-less.go 
package main

import (
        "bufio"
        "fmt"
        "log"
        "os"
        "sort"
        "strconv"
        "strings"
)

func ReadInput() []int {
        var text string
        scanner := bufio.NewScanner(os.Stdin)
        fmt.Print("Please, input digits one by one divided by space (lets try to find the smallest one): ")
        scanner.Scan()
        text = scanner.Text()

        //fmt.Println(text)
        tmp := strings.Fields(text)

        values := make([]int, 0, len(tmp))
        for _, raw := range tmp {
                v, err := strconv.Atoi(raw)
                if err != nil {
                        log.Print(err)
                        continue
                }
                values = append(values, v)
        }
        return values
}

func main() {
        lines := ReadInput()
        sorted := lines
        //fmt.Println(lines)
        sort.Ints(sorted)
        fmt.Println("The smallest one is: ", sorted[0])
}
root@dev1-10:~/netol_do/go# 

```

1. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть `(3, 6, 9, …)`.

В виде решения ссылку на код или сам код. 

```bash

root@dev1-10:~/netol_do/go# go run print-100.go 
3 /3= 1 
6 /3= 2 
9 /3= 3 
12 /3= 4 
15 /3= 5 
18 /3= 6 
21 /3= 7 
24 /3= 8 
27 /3= 9 
30 /3= 10 
33 /3= 11 
36 /3= 12 
39 /3= 13 
42 /3= 14 
45 /3= 15 
48 /3= 16 
51 /3= 17 
54 /3= 18 
57 /3= 19 
60 /3= 20 
63 /3= 21 
66 /3= 22 
69 /3= 23 
72 /3= 24 
75 /3= 25 
78 /3= 26 
81 /3= 27 
84 /3= 28 
87 /3= 29 
90 /3= 30 
93 /3= 31 
96 /3= 32 
99 /3= 33 
Total  33  multiple of 3 in range 1..100
root@dev1-10:~/netol_do/go# cat print-100.go 
package main

func main() {
        n := 0
        for i := 3; i <= 100; i += 3 {
                print(i, " /3= ", i/3, " \n")
                n += 1
        }
        println("Total ", n, " multiple of 3 in range 1..100")
}
root@dev1-10:~/netol_do/go# 

```

## Задача 4. Протестировать код (не обязательно).

Создайте тесты для функций из предыдущего задания. 

```bash

root@dev1-10:~/netol_do/go/print-100# go run print-100.go
6 /6= 1 
12 /6= 2 
18 /6= 3 
24 /6= 4 
30 /6= 5 
36 /6= 6 
42 /6= 7 
48 /6= 8 
54 /6= 9 
60 /6= 10 
66 /6= 11 
72 /6= 12 
78 /6= 13 
84 /6= 14 
90 /6= 15 
96 /6= 16 
Total  16  figures multiple of  6  in range  1 .. 100
[6 12 18 24 30 36 42 48 54 60 66 72 78 84 90 96]
root@dev1-10:~/netol_do/go/print-100# go test 
7 /7= 1 
14 /7= 2 
21 /7= 3 
28 /7= 4 
35 /7= 5 
42 /7= 6 
49 /7= 7 
56 /7= 8 
63 /7= 9 
70 /7= 10 
77 /7= 11 
84 /7= 12 
91 /7= 13 
98 /7= 14 
Total  14  figures multiple of  7  in range  1 .. 100
[7 14 21 28 35 42 49 56 63 70 77 84 91 98]
0 -й элемент - ok!
1 -й элемент - ok!
2 -й элемент - ok!
3 -й элемент - ok!
4 -й элемент - ok!
5 -й элемент - ok!
6 -й элемент - ok!
7 -й элемент - ok!
8 -й элемент - ok!
9 -й элемент - ok!
10 -й элемент - ok!
11 -й элемент - ok!
12 -й элемент - ok!
13 -й элемент - ok!
PASS
ok      example/m-to-ft/print-100       0.005s
root@dev1-10:~/netol_do/go/print-100# go test 
9 /9= 1 
18 /9= 2 
27 /9= 3 
36 /9= 4 
45 /9= 5 
54 /9= 6 
63 /9= 7 
72 /9= 8 
81 /9= 9 
90 /9= 10 
99 /9= 11 
Total  11  figures multiple of  9  in range  1 .. 100
[9 18 27 36 45 54 63 72 81 90 99]
6 -й элемент - ok!
--- FAIL: TestPrint_100 (0.00s)
    print-100_test.go:17: 0 -й элемент со значением  9  не делится без остатка на 7 !
    print-100_test.go:17: 1 -й элемент со значением  18  не делится без остатка на 7 !
    print-100_test.go:17: 2 -й элемент со значением  27  не делится без остатка на 7 !
    print-100_test.go:17: 3 -й элемент со значением  36  не делится без остатка на 7 !
    print-100_test.go:17: 4 -й элемент со значением  45  не делится без остатка на 7 !
    print-100_test.go:17: 5 -й элемент со значением  54  не делится без остатка на 7 !
    print-100_test.go:17: 7 -й элемент со значением  72  не делится без остатка на 7 !
    print-100_test.go:17: 8 -й элемент со значением  81  не делится без остатка на 7 !
    print-100_test.go:17: 9 -й элемент со значением  90  не делится без остатка на 7 !
    print-100_test.go:17: 10 -й элемент со значением  99  не делится без остатка на 7 !
FAIL
exit status 1
FAIL    example/m-to-ft/print-100       0.006s
root@dev1-10:~/netol_do/go/print-100# 
```

```go
root@dev1-10:~/netol_do/go/print-100# cat print-100.go
package main

import "fmt"

func Print_100(s int, e int, d int) []int {
        //e - end range
        //d - step, multiple of
        //s - start range
        n := 0
        var output []int
        for i := d; i <= e; i += d {
                print(i, " /", d, "= ", i/d, " \n")
                n += 1
                output = append(output, i)
        }
        println("Total ", n, " figures multiple of ", d, " in range ", s, "..", e)
        return output
}

func main() {
        v := Print_100(1, 100, 6)
        fmt.Println(v)
}
```
```go
root@dev1-10:~/netol_do/go/print-100# cat print-100_test.go
package main

import (
        "fmt"
        "testing"
)

func TestPrint_100(t *testing.T) {
        //testing func Print_100 in package main, TestXxx - case sensitive!
        var v []int
        v = Print_100(1, 100, 9)
        d := 7
        fmt.Println(v)

        for i, r := range v {
                if r%d != 0 {
                        t.Error(i, "-й элемент со значением ", r, " не делится без остатка на", d, "!")
                } else {
                        println(i, "-й элемент - ok!")
                }
        }
}


```



---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---

