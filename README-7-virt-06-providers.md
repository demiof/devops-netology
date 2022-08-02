# Домашнее задание к занятию "7.6. Написание собственных провайдеров для Terraform."

Бывает, что 
* общедоступная документация по терраформ ресурсам не всегда достоверна,
* в документации не хватает каких-нибудь правил валидации или неточно описаны параметры,
* понадобиться использовать провайдер без официальной документации,
* может возникнуть необходимость написать свой провайдер для системы используемой в ваших проектах.   

## Задача 1. 
Давайте потренируемся читать исходный код AWS провайдера, который можно склонировать от сюда: 
[   ](https://github.com/hashicorp/terraform-provider-aws.git).
Просто найдите нужные ресурсы в исходном коде и ответы на вопросы станут понятны.  


1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе.   

<!--
```bash


root@dev1-10:~/aws/terraform-provider-aws# grep -cR -A 15  "resource \"" ./ | grep -v ":0" | awk -F ":" '{print $1, $2}' | grep 97

root@dev1-10:~/aws/terraform-provider-aws# grep -cR -A 15  "resource \"" ./ | grep -v ":0" | awk -F ":" '{print $1, $2}' | grep " 97"
./internal/service/s3/bucket_test.go 97
./internal/service/ec2/vpc_route_table_test.go 97

```
[https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/service/ec2/vpc_route_table_test.go](https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/service/ec2/vpc_route_table_test.go)

-->
> Если же анализировать, то вроде как делается мап на тип string в схемах DataSource и Resourse тут:

[https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/provider/provider.go](https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/provider/provider.go)

> Сам же DataSource aws_sqs_queue описан тут: 

```bash

root@dev1-10:~/aws/terraform-provider-aws/internal/provider# grep -cinR ResourceQueue ../ | grep -v :0 | grep -v .*\.swp
../service/mediaconvert/queue.go:11
../service/sqs/queue_test.go:2
../service/sqs/sweep.go:1
../service/sqs/queue.go:15
../service/sqs/queue_policy_test.go:2
../service/sqs/queue_policy.go:9
../service/connect/queue_test.go:1
../service/connect/queue.go:9
../provider/provider.go:4


```
<!--
```bash

root@dev1-10:~/aws/terraform-provider-aws# grep -cR -A 15  "data \"" ./ | grep -v ":0" | awk -F ":" '{print $1, $2}' | grep 77
./internal/service/rds/instance_test.go 77
root@dev1-10:~/aws/terraform-provider-aws# vim ./internal/service/rds/instance_test.go

```
[https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/service/rds/instance_test.go](https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/service/rds/instance_test.go)
-->

1. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`. 
    * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.





<!--
> Параметр`name` по всей видимости может (должен) конфликтовать с `arn`, что похоже из условия ниже в цикле по массиву attrName. Т.е. если не выполняется условие ниже, то fmt выводит ошибку "attrName is {значение его в rs.Primary.Attributes}; want {значение его в sqsQueueRs.Primary.Attributes} :

```go

if rs.Primary.Attributes[attrName] != sqsQueueRs.Primary.Attributes[attrName] {
                                return fmt.Errorf(
                                        "%s is %s; want %s",
                                        attrName,
                                        rs.Primary.Attributes[attrName],
                                        sqsQueueRs.Primary.Attributes[attrName],
                                )
```

> искал так:


```bash

root@dev1-10:~/aws/terraform-provider-aws# grep -R -A 5 'resource "aws_sqs_queue"' . | grep -c 'name = '
33
root@dev1-10:~/aws/terraform-provider-aws# grep -R -A 5 'resource "aws_sqs_queue"' . | grep 'name = '
./website/docs/r/sns_topic_subscription.html.markdown-  name = "user-updates-queue"
./website/docs/r/sqs_queue_policy.html.markdown-  name = "examplequeue"
./website/docs/r/sqs_queue.html.markdown-  name = "terraform-example-deadletter-queue"
./website/docs/r/s3_bucket_notification.html.markdown-  name = "s3-event-notification-queue"
./website/docs/r/s3_bucket_notification.html.markdown-  name = "s3-event-notification-queue"
./internal/service/s3/bucket_notification_test.go-  name = %[1]q
./internal/service/elasticbeanstalk/environment_test.go-  name = %[1]q
./internal/service/sqs/queue_test.go-  name = %[1]q
./internal/service/sqs/queue_test.go-  name = %[1]q
./internal/service/sqs/queue_test.go-  name = %[1]q
./internal/service/sqs/queue_test.go-  name = "%[1]s-2"
./internal/service/sqs/queue_test.go-  name = "%[1]s-2"
./internal/service/sqs/queue_policy_test.go-  name = %[1]q
./internal/service/sqs/queue_policy_test.go-  name = %[1]q
./internal/service/sqs/queue_data_source_test.go-  name = "%[1]s_wrong"
./internal/service/sqs/queue_data_source_test.go-  name = "%[1]s"
./internal/service/sqs/queue_data_source_test.go-  name = aws_sqs_queue.test.name
./internal/service/sqs/queue_data_source_test.go-  name = "%[1]s"
./internal/service/sns/topic_subscription_test.go-  name = %[1]q
./internal/service/sns/topic_subscription_test.go-  name = %[1]q
./internal/service/sns/topic_subscription_test.go-  name = %[1]q
./internal/service/sns/topic_subscription_test.go-  name = %[1]q
./internal/service/sns/topic_subscription_test.go-  name = %[2]q
./internal/service/sns/topic_subscription_test.go-  name = %[1]q
./internal/service/apigatewayv2/integration_test.go-  name = "%[1]s-${count.index}"
./internal/service/glue/crawler_test.go-  name = %[1]q
./internal/service/glue/crawler_test.go-  name = %[1]q
./internal/service/glue/crawler_test.go-  name = "%[1]sdlq"
./internal/service/lambda/event_source_mapping_test.go-  name = %[1]q
./internal/service/lambda/function_event_invoke_config_test.go-  name = %[1]q
./internal/service/lambda/function_event_invoke_config_test.go-  function_name = aws_lambda_function.test.function_name
./internal/service/lambda/function_event_invoke_config_test.go-  name = %[1]q
./internal/service/lambda/function_event_invoke_config_test.go-  function_name = aws_lambda_function.test.function_name
root@dev1-10:~/aws/terraform-provider-aws# vim ./internal/service/sqs/queue_data_source_test.go

```



```go

func testAccQueueCheckDataSource(datasourceName, resourceName string) resource.TestCheckFunc {
        return func(s *terraform.State) error {
                rs, ok := s.RootModule().Resources[datasourceName]
                if !ok {
                        return fmt.Errorf("root module has no resource called %s", datasourceName)
                }

                sqsQueueRs, ok := s.RootModule().Resources[resourceName]
                if !ok {
                        return fmt.Errorf("root module has no resource called %s", resourceName)
                }

                attrNames := []string{
                        "arn",
                        "name",
                }

                for _, attrName := range attrNames {
                        if rs.Primary.Attributes[attrName] != sqsQueueRs.Primary.Attributes[attrName] {
                                return fmt.Errorf(
                                        "%s is %s; want %s",
                                        attrName,
                                        rs.Primary.Attributes[attrName],
                                        sqsQueueRs.Primary.Attributes[attrName],
                                )
                        }
                }

                return nil
        }

```
-->

    * Какая максимальная длина имени? 

<!--
> Выходит 80 символов:

```bash

root@dev1-10:~/aws/terraform-provider-aws# grep '`name` -'  ./website/docs/r/sqs_queue.html.markdown 
* `name` - (Optional) The name of the queue. Queue names must be made up of only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 80 characters long. For a FIFO (first-in-first-out) queue, the name must end with the `.fifo` suffix. If omitted, Terraform will assign a random, unique name. Conflicts with `name_prefix`

```
-->
    * Какому регулярному выражению должно подчиняться имя? 

> Нашел для "name" валидирование по длине и регексп тут:

```bash

terraform-provider-aws/internal/service/schemas/schema.go

```

```go

			"name": {
				Type:     schema.TypeString,
				Required: true,
				ForceNew: true,
				ValidateFunc: validation.All(
					validation.StringLenBetween(1, 385),
					validation.StringMatch(regexp.MustCompile(`^[\.\-_A-Za-z@]+`), ""),
				),
			},

```

> Нашел для "name" с кес конфликтует тут:  

```bash

terraform-provider-aws/internal/service/sqs/queue.go

```

```go
		"name": {
			Type:          schema.TypeString,
			Optional:      true,
			Computed:      true,
			ForceNew:      true,
			ConflictsWith: []string{"name_prefix"},
		},
		"name_prefix": {
			Type:          schema.TypeString,
			Optional:      true,
			Computed:      true,
			ForceNew:      true,
			ConflictsWith: []string{"name"},
``` 
> и 

```go
ValidateFunc: validation.StringLenBetween(1,127);
```

<!--
> Исходя из предыдущего, маленькие и Большие ASCII символы, цифры, подчеркивания и тире: ^[\d\w\_\-]{1,80}$
-->


## Задача 2. (Не обязательно) 
В рамках вебинара и презентации мы разобрали как создать свой собственный провайдер на примере кофемашины. 
Также вот официальная документация о создании провайдера: 
[https://learn.hashicorp.com/collections/terraform/providers](https://learn.hashicorp.com/collections/terraform/providers).

1. Проделайте все шаги создания провайдера.
2. В виде результата приложение ссылку на исходный код.

[https://github.com/demiof/terraform-provider-hashicups/tree/v0.2.1](https://github.com/demiof/terraform-provider-hashicups/tree/v0.2.1)

3. Попробуйте скомпилировать провайдер, если получится то приложите снимок экрана с командой и результатом компиляции.   

```bash

root@dev1-10:~/providers/terraform-provider-hashicups# ll
total 108K
drwxr-xr-x 10 root root 4.0K Jul 30 10:52 .
drwxr-xr-x  4 root root 4.0K Jul 28 07:46 ..
drwxr-xr-x  2 root root 4.0K Jul 26 18:47 docker_compose
drwxr-xr-x  4 root root 4.0K Jul 30 10:48 docs
drwxr-xr-x  5 root root 4.0K Jul 30 10:25 examples
drwxr-xr-x  8 root root 4.0K Jul 30 11:11 .git
drwxr-xr-x  3 root root 4.0K Jul 30 10:52 .github
-rw-r--r--  1 root root 1.4K Jul 26 18:47 .gitignore
-rw-r--r--  1 root root 3.3K Jul 30 10:41 go.mod
-rw-r--r--  1 root root 1.8K Jul 30 10:51 .goreleaser.yml
-rw-r--r--  1 root root  35K Jul 30 10:41 go.sum
drwxr-xr-x  2 root root 4.0K Jul 30 08:47 hashicups
-rw-r--r--  1 root root  470 Jul 30 10:44 main.go
-rw-r--r--  1 root root 1.6K Jul 26 18:51 Makefile
-rw-r--r--  1 root root  376 Jul 26 18:47 README.md
-rw-r--r--  1 root root   83 Jul 30 10:51 terraform-registry-manifest.json
-rw-r--r--  1 root root  155 Jul 30 09:11 terraform.tfstate
drwxr-xr-x  2 root root 4.0K Jul 30 10:42 tools
drwxr-xr-x  5 root root 4.0K Jul 30 10:46 vendor
root@dev1-10:~/providers/terraform-provider-hashicups# go build -o terraform-provider-hashicups
root@dev1-10:~/providers/terraform-provider-hashicups# ll
total 20M
drwxr-xr-x 10 root root 4.0K Jul 30 11:42 .
drwxr-xr-x  4 root root 4.0K Jul 28 07:46 ..
drwxr-xr-x  2 root root 4.0K Jul 26 18:47 docker_compose
drwxr-xr-x  4 root root 4.0K Jul 30 10:48 docs
drwxr-xr-x  5 root root 4.0K Jul 30 10:25 examples
drwxr-xr-x  8 root root 4.0K Jul 30 11:42 .git
drwxr-xr-x  3 root root 4.0K Jul 30 10:52 .github
-rw-r--r--  1 root root 1.4K Jul 26 18:47 .gitignore
-rw-r--r--  1 root root 3.3K Jul 30 10:41 go.mod
-rw-r--r--  1 root root 1.8K Jul 30 10:51 .goreleaser.yml
-rw-r--r--  1 root root  35K Jul 30 10:41 go.sum
drwxr-xr-x  2 root root 4.0K Jul 30 08:47 hashicups
-rw-r--r--  1 root root  470 Jul 30 10:44 main.go
-rw-r--r--  1 root root 1.6K Jul 26 18:51 Makefile
-rw-r--r--  1 root root  376 Jul 26 18:47 README.md
-rwxr-xr-x  1 root root  20M Jul 30 11:42 terraform-provider-hashicups
-rw-r--r--  1 root root   83 Jul 30 10:51 terraform-registry-manifest.json
-rw-r--r--  1 root root  155 Jul 30 09:11 terraform.tfstate
drwxr-xr-x  2 root root 4.0K Jul 30 10:42 tools
drwxr-xr-x  5 root root 4.0K Jul 30 10:46 vendor
root@dev1-10:~/providers/terraform-provider-hashicups# 
```
---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
