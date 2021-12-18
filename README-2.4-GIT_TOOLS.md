# Выполнение ДЗ 2.4 - Инструмнты Git:


## № 1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.

> Вариант1 - не совсем верный, как оказалось, т.к. git log --oneline выводит постранично, и найденный ниже хэш, видимо был на первой странице)

	root@dev1-10:/home/demi/netol_do/terraform# git log --oneline | grep aefea
	aefead220 Update CHANGELOG.md

>> Передаем результаты вывода в grep и просматриваем объект по части хэша коммита. Находим полный хэш: 

	root@dev1-10:/home/demi/netol_do/terraform# git show aefead220
	commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
	Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
	Date:   Thu Jun 18 10:29:58 2020 -0400

	Update CHANGELOG.md

	diff --git a/CHANGELOG.md b/CHANGELOG.md
	index 86d70e3e0..588d807b1 100644
	--- a/CHANGELOG.md
	+++ b/CHANGELOG.md
	@@ -27,6 +27,7 @@ BUG FIXES:
 	* backend/s3: Prefer AWS shared configuration over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
 	* backend/s3: Prefer ECS credentials over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
 	* backend/s3: Remove hardcoded AWS Provider messaging ([#25134](https://github.com/hashicorp/terraform/issues/25134))
	+* command: Fix bug with global `-v`/`-version`/`--version` flags introduced in 0.13.0beta2 [GH-25277]
 	* command/0.13upgrade: Fix `0.13upgrade` usage help text to include options ([#25127](https://github.com/hashicorp/terraform/issues/25127))
 	* command/0.13upgrade: Do not add source for builtin provider ([#25215](https://github.com/hashicorp/terraform/issues/25215))
 	* command/apply: Fix bug which caused Terraform to silently exit on Windows when using absolute plan path ([#25233](https://github.com/hashicorp/terraform/issues/25233))

>Вариант2 - верный, с генерацией патча, если не указать -1 после -p не отфильтруется вывод после вхождения 'aefea' 

 root@dev1-10:/home/demi/netol_do/terraform# git log -p -1 aefea
 commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
 Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
 Date:   Thu Jun 18 10:29:58 2020 -0400
 
     Update CHANGELOG.md
 
 diff --git a/CHANGELOG.md b/CHANGELOG.md
 index 86d70e3e0..588d807b1 100644
 --- a/CHANGELOG.md
 +++ b/CHANGELOG.md
 @@ -27,6 +27,7 @@ BUG FIXES:
  * backend/s3: Prefer AWS shared configuration over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
  * backend/s3: Prefer ECS credentials over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
  * backend/s3: Remove hardcoded AWS Provider messaging ([#25134](https://github.com/hashicorp/terraform/issues/25134))
 +* command: Fix bug with global `-v`/`-version`/`--version` flags introduced in 0.13.0beta2 [GH-25277]
  * command/0.13upgrade: Fix `0.13upgrade` usage help text to include options ([#25127](https://github.com/hashicorp/terraform/issues/25127))
  * command/0.13upgrade: Do not add source for builtin provider ([#25215](https://github.com/hashicorp/terraform/issues/25215))
  * command/apply: Fix bug which caused Terraform to silently exit on Windows when using absolute plan path ([#25233](https://github.com/hashicorp/terraform/issues/25233)) 



## 2. Какому тегу соответствует коммит 85024d3?

 git log -p -1 85024d3


 tag: v0.12.23

> Почему-то не получилось(: git log -p -1 85024d3 | grep -e "\(tag: [a-zA-Z]{0}(.[0-9]{0,4}){0,10}\)$"



## 3. Сколько родителей у коммита b8d720? Напишите их хэши. 


	root@dev1-10:/home/demi/netol_do/terraform# git log b8d720 -4 --oneline --graph
	*   b8d720f83 Merge pull request #23916 from hashicorp/cgriggs01-stable
	|\  
	| * 9ea88f22f add/update community provider listings
	|/  
	*   56cd7859e Merge pull request #23857 from hashicorp/cgriggs01-stable
	|\  
	| * ffbcf5581 [Website]add checkpoint links
	|/  
 
 
> 2 родителя с хэшами: 9ea88f22f,  56cd7859e  



## 4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.

	root@dev1-10:/home/demi/netol_do/terraform# git log v0.12.24 ^v0.12.22
	commit 33ff1c03bb960b332be3af2e333462dde88b279e (tag: v0.12.24)
	Author: tf-release-bot <terraform@hashicorp.com>
	Date:   Thu Mar 19 15:04:05 2020 +0000
 
	v0.12.24
 
 	commit b14b74c4939dcab573326f4e3ee2a62e23e12f89
	Author: Chris Griggs <cgriggs@hashicorp.com>
	Date:   Tue Mar 10 08:59:20 2020 -0700
 
	[Website] vmc provider links
 
	commit 3f235065b9347a758efadc92295b540ee0a5e26e
	Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
	Date:   Thu Mar 19 10:39:31 2020 -0400
	 
	Update CHANGELOG.md
 
 	commit 6ae64e247b332925b872447e9ce869657281c2bf
	Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
	Date:   Thu Mar 19 10:20:10 2020 -0400
 	
	registry: Fix panic when server is unreachable
	
	Non-HTTP errors previously resulted in a panic due to dereferencing the
	resp pointer while it was nil, as part of rendering the error message.
	This commit changes the error message formatting to cope with a nil
	response, and extends test coverage.
	
	Fixes #24384
	 
	commit 5c619ca1baf2e21a155fcdb4c264cc9e24a2a353
	Author: Nick Fagerlund <nick.fagerlund@gmail.com>
	Date:   Wed Mar 18 12:30:20 2020 -0700
	
	website: Remove links to the getting started guide's old location
	
	Since these links were in the soon-to-be-deprecated 0.11 language section, I
	think we can just remove them without needing to find an equivalent li.
		
	commit 06275647e2b53d97d4f0a19a0fec11f6d69820b5
	Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
	Date:   Wed Mar 18 10:57:06 2020 -0400
	
	Update CHANGELOG.md
	 
	commit d5f9411f5108260320064349b757f55c09bc4b80
	Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
	Date:   Tue Mar 17 13:21:35 2020 -0400
	 
	command: Fix bug when using terraform login on Windows
	 
	commit 4b6d06cc5dcb78af637bbb19c198faff37a066ed
	Author: Pam Selle <pam@hashicorp.com>
	Date:   Tue Mar 10 12:04:50 2020 -0400
	
	Update CHANGELOG.md
 
	commit dd01a35078f040ca984cdd349f18d0b67e486c35
	Author: Kristin Laemmert <mildwonkey@users.noreply.github.com>
	Date:   Thu Mar 5 16:32:43 2020 -0500
 
	Update CHANGELOG.md
 
	commit 225466bc3e5f35baa5d07197bbc079345b77525e
	Author: tf-release-bot <terraform@hashicorp.com>
	Date:   Thu Mar 5 21:12:06 2020 +0000
 
	Cleanup after v0.12.23 release
	 
	commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
	Author: tf-release-bot <terraform@hashicorp.com>
	Date:   Thu Mar 5 20:56:10 2020 +0000
	 
	v0.12.23
	 
	commit 4703cb6c1c7a00137142da867588a5752c54fa6a
	Author: Kristin Laemmert <mildwonkey@users.noreply.github.com>
	Date:   Thu Mar 5 15:27:37 2020 -0500
	 
	Update CHANGELOG.md
	 
	commit 0b4470e0d45b2818f385eee5daf0816838de84ef
	Author: tf-release-bot <terraform@hashicorp.com>
	Date:   Thu Mar 5 20:24:20 2020 +0000
	 
	Cleanup after v0.12.22 release


## 5. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).

> Ищем файл, где определялась providerSource()

	root@dev1-10:/home/demi/netol_do/terraform# git grep -p 'func providerSource(' .
	provider_source.go=import (
	provider_source.go:func providerSource(configs []*cliconfig.ProviderInstallation, services *disco.Disco) (getproviders.Source, tfdiags.Diagnostics) {
	root@dev1-10:/home/demi/netol_do/terraform#

> Это файл provider_source,go
> Далее по журналу изменения строки:

	git log -L :providerSource:provider_source.go
	commit 8c928e83589d90a031f811fae52a81be7153e82f
	Author: Martin Atkins <mart@degeneration.co.uk>
	Date:   Thu Apr 2 18:04:39 2020 -0700

## 6. Найдите все коммиты в которых была изменена функция globalPluginDirs.

	git log -SglobalPluginDirs | grep -w -e 'commit'
	commit 35a058fb3ddfae9cfee0b3893822c9a95b920f4c
	commit c0b17610965450a89598da491ce9b6b5cbd6393f
	commit 8364383c359a6b738a436d1b7745ccdce178df47


## 7. Кто автор функции synchronizedWriters?

> Возможно найти только с помощью поиска по журналу, т.к. данная функция вместе с файлом была удалена:

	git log -S synchronizedWriters

> Первым, где она упоминалась был commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5 

	git show 5ac311e2a91e381e2f52234668b49ba670aa0fe5
	 
	commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5
	Author: Martin Atkins <mart@degeneration.co.uk>
	Date:   Wed May 3 16:25:41 2017 -0700

 	...


> На всякий случай, удостоверяемся, что данного файла действительно нет в раб. папке на тек. момент:

	find . -name synchronized_writers.go
