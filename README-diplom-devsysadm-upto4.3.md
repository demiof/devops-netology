# Курсовая работа по итогам модуля "DevOps и системное администрирование"

Курсовая работа необходима для проверки практических навыков, полученных в ходе прохождения курса "DevOps и системное администрирование".

Мы создадим и настроим виртуальное рабочее место. Позже вы сможете использовать эту систему для выполнения домашних заданий по курсу

## Задание

1. Создайте виртуальную машину Linux.


```bash


Bringing machine 'netodo-3' up with 'virtualbox' provider...
==> netodo-3: Preparing master VM for linked clones...
    netodo-3: This is a one time operation. Once the master VM is prepared,
    netodo-3: it will be used as a base for linked clones, making the creation
    netodo-3: of new VMs take milliseconds on a modern system.
==> netodo-3: Importing base box 'bento/ubuntu-20.04'...
==> netodo-3: Cloning VM...
==> netodo-3: Matching MAC address for NAT networking...
==> netodo-3: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> netodo-3: There was a problem while downloading the metadata for your box
==> netodo-3: to check for updates. This is not an error, since it is usually due
==> netodo-3: to temporary network problems. This is just a warning. The problem
==> netodo-3: encountered was:
==> netodo-3:
==> netodo-3: The requested URL returned error: 404
==> netodo-3:
==> netodo-3: If you want to check for box updates, verify your network connection
==> netodo-3: is valid and try again.
==> netodo-3: Setting the name of the VM: odines0.linkintel.ru
==> netodo-3: Clearing any previously set network interfaces...
==> netodo-3: Preparing network interfaces based on configuration...
    netodo-3: Adapter 1: nat
    netodo-3: Adapter 2: bridged
    netodo-3: Adapter 3: hostonly
==> netodo-3: Forwarding ports...
    netodo-3: 80 (guest) => 8083 (host) (adapter 1)
    netodo-3: 22 (guest) => 2223 (host) (adapter 1)
==> netodo-3: Running 'pre-boot' VM customizations...
==> netodo-3: Booting VM...
==> netodo-3: Waiting for machine to boot. This may take a few minutes...
    netodo-3: SSH address: 127.0.0.1:2223
    netodo-3: SSH username: vagrant
    netodo-3: SSH auth method: private key
    netodo-3:
    netodo-3: Vagrant insecure key detected. Vagrant will automatically replace
    netodo-3: this with a newly generated keypair for better security.
    netodo-3:
    netodo-3: Inserting generated public key within guest...
    netodo-3: Removing insecure key from the guest if it's present...
    netodo-3: Key inserted! Disconnecting and reconnecting using new SSH key...
==> netodo-3: Machine booted and ready!
==> netodo-3: Checking for guest additions in VM...
==> netodo-3: Setting hostname...
==> netodo-3: Configuring and enabling network interfaces...
==> netodo-3: Mounting shared folders...
    netodo-3: /vagrant => C:/Users/demi/VirtualBox VMs/Vagrant

```




2. Установите ufw и разрешите к этой машине сессии на порты 22 и 443, при этом трафик на интерфейсе localhost (lo) должен ходить свободно на все порты.

```bash

root@odines0:~# ufw allow 22/tcp
Rules updated
Rules updated (v6)
root@odines0:~# ufw allow 443/tcp
Rules updated
Rules updated (v6)


root@odines0:~# ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)

root@odines0:~# ufw default deny incoming
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)
root@odines0:~# ufw status
Status: active


root@odines0:~# ufw default deny incoming
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)
root@odines0:~# ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)


root@odines0:~# ufw allow in on lo
Rule added
Rule added (v6)
root@odines0:~# ufw status numbered
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere
[ 2] 443/tcp                    ALLOW IN    Anywhere
[ 3] Anywhere on lo             ALLOW IN    Anywhere
[ 4] 22/tcp (v6)                ALLOW IN    Anywhere (v6)
[ 5] 443/tcp (v6)               ALLOW IN    Anywhere (v6)
[ 6] Anywhere (v6) on lo        ALLOW IN    Anywhere (v6)


```



3. Установите hashicorp vault ([инструкция по ссылке](https://learn.hashicorp.com/tutorials/vault/getting-started-install?in=vault/getting-started#install-vault)).

```bash


root@dev1-10:~/hideme# snap install vault
vault (1.5/stable) 1.5.9 from Canonical✓ installed


```

4. Cоздайте центр сертификации по инструкции ([ссылка](https://learn.hashicorp.com/tutorials/vault/pki-engine?in=vault/secrets-management)) и выпустите сертификат для использования его в настройке веб-сервера nginx (срок жизни сертификата - месяц).
5. Установите корневой сертификат созданного центра сертификации в доверенные в хостовой системе.


```bash

 1607  18.04.2022 20:44:28: export VAULT_ADDR=http://127.0.0.1:8200
 1608  18.04.2022 20:44:32: export VAULT_TOKEN=root
 1609  18.04.2022 20:45:07: vault secrets enable pki
 1610  18.04.2022 20:45:15: vault secrets tune -max-lease-ttl=87600h pki
 1611  18.04.2022 20:45:23: vault write -field=certificate pki/root/generate/internal common_name="linkintel.ru" ttl=87600h > CA_cert_linkintel.ru.crt
 1612  18.04.2022 20:45:41: vault write pki/config/urls issuing_certificates="$VAULT_ADDR/v1/pki/ca" crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
 1613  18.04.2022 20:46:01: vault secrets enable -path=pki_int pki
 1614  18.04.2022 20:46:05: vault secrets tune -max-lease-ttl=43800h pki_int
 1615  18.04.2022 20:46:42: vault write -format=json pki_int/intermediate/generate/internal common_name="linkintel.ru Intermediate Authority"      | jq -r '.data.csr' > pki_intermediate_linkintel.ru.csr
 1616  18.04.2022 20:47:45: vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate_linkintel.ru.csr format=pem_bundle ttl="43800h"      | jq -r '.data.certificate' > intermediate.cert_linkintel.ru.pem
 1617  18.04.2022 20:48:28: vault write pki_int/intermediate/set-signed certificate=@intermediate.cert_linkintel.ru.pem
 1618  18.04.2022 20:51:21: vault write pki_int/roles/example-dot-com allowed_domains="linkintel.ru" allow_subdomains=true max_ttl="720h"
 1619  18.04.2022 20:51:57: vault write pki_int/issue/example-dot-com common_name="test.linkintel.ru" ttl="24h"
 1620  18.04.2022 20:56:53: vault write pki_int/revoke serial_number=09:58:1e:43:23:69:b1:40:86:10:9a:f8:02:9b:d8:33:7d:f6:23:3b
 1621  18.04.2022 20:57:34: vault write pki_int/tidy tidy_cert_store=true tidy_revoked_certs=true
 1622  18.04.2022 21:00:07: snap install nginx




```

6. Установите nginx.

```bash





root@dev1-10:~# apt-get install nginx
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
nginx is already the newest version (1.18.0-6.1).
0 upgraded, 0 newly installed, 0 to remove and 116 not upgraded.
root@dev1-10:~# 






```


7. По инструкции ([ссылка](https://nginx.org/en/docs/http/configuring_https_servers.html)) настройте nginx на https, используя ранее подготовленный сертификат:
  - можно использовать стандартную стартовую страницу nginx для демонстрации работы сервера;
  - можно использовать и другой html файл, сделанный вами;



```bash
	$1=test.linkintel.ru
        export VAILT_ADDR='http://127.0.0.1:8200'
        export VAULT_TOKEN='root'

        #generate root cert authority
        cd /root/vault
        vault secrets enable pki
        vault secrets tune -max-lease-ttl=87600h pki
        vault write -field=certificate pki/root/generate/internal common_name=test.linkintel.ru ttl=87600h > CA_cert_test.linkintel.ru.crt
        vault write pki/config/urls issuing_certificates="$VAULT_ADDR/v1/pki/ca" crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
        #generate intermediate ca
        vault secrets enable -path=pki_int pki
        vault secrets tune -max-lease-ttl=43800h pki_int
        vault write -format=json pki_int/intermediate/generate/internal common_name="test.test.linkintel.ru Intermediate Authority" | jq -r '.data.csr' > pki_intermediate.test.linkintel.ru.csr
        vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.test.linkintel.ru.csr format=pem_bundle ttl="43800h" | jq -r '.data.certificate' > intermediate.cert.test.linkintel.ru.pem
        vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.test.linkintel.ru.pem
        #create role
        vault write pki_int/roles/linkintel-dot-ru allowed_domains=linkintel.ru allow_subdomains=true max_ttl="720h"
        #request cert
        vault write pki_int/issue/linkintel-dot-ru common_name=test.linkintel.ru ttl="24h" 
```





8. Откройте в браузере на хосте https адрес страницы, которую обслуживает сервер nginx.


```bash



root@dev1-10:/home/demi/netol_do/devops-netology# wget https://127.0.0.1:444
--2022-04-24 08:50:55--  https://127.0.0.1:444/
Connecting to 127.0.0.1:444... connected.
ERROR: The certificate of ‘127.0.0.1’ is not trusted.
ERROR: The certificate of ‘127.0.0.1’ doesn't have a known issuer.
The certificate's owner does not match hostname ‘127.0.0.1’
root@dev1-10:/home/demi/netol_do/devops-netology# man wget
root@dev1-10:/home/demi/netol_do/devops-netology# 
root@dev1-10:/home/demi/netol_do/devops-netology# wget --no-check-certificate https://127.0.0.1:444
--2022-04-24 08:52:11--  https://127.0.0.1:444/
Connecting to 127.0.0.1:444... connected.
WARNING: The certificate of ‘127.0.0.1’ is not trusted.
WARNING: The certificate of ‘127.0.0.1’ doesn't have a known issuer.
The certificate's owner does not match hostname ‘127.0.0.1’
HTTP request sent, awaiting response... 200 OK
Length: 10701 (10K) [text/html]
Saving to: ‘index.html’

index.html                               100%[==================================================================================>]  10.45K  --.-KB/s    in 0s      

2022-04-24 08:52:11 (111 MB/s) - ‘index.html’ saved [10701/10701]

root@dev1-10:/home/demi/netol_do/devops-netology# echo index.html 
index.html
root@dev1-10:/home/demi/netol_do/devops-netology# ls -la  index.html 
-rw-r--r-- 1 root root 10701 Dec  9 10:27 index.html
root@dev1-10:/home/demi/netol_do/devops-netology# cat  index.html 

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Apache2 Debian Default Page: It works</title>
    <style type="text/css" media="screen">
  * {
    margin: 0px 0px 0px 0px;
    padding: 0px 0px 0px 0px;
  }

  body, html {
    padding: 3px 3px 3px 3px;

    background-color: #D8DBE2;

    font-family: Verdana, sans-serif;
    font-size: 11pt;
    text-align: center;
  }

  div.main_page {
    position: relative;
    display: table;

    width: 800px;

    margin-bottom: 3px;
    margin-left: auto;
    margin-right: auto;
    padding: 0px 0px 0px 0px;

    border-width: 2px;
    border-color: #212738;
    border-style: solid;

    background-color: #FFFFFF;

    text-align: center;
  }

  div.page_header {
    height: 99px;
    width: 100%;

    background-color: #F5F6F7;
  }

  div.page_header span {
    margin: 15px 0px 0px 50px;

    font-size: 180%;
    font-weight: bold;
  }

  div.page_header img {
    margin: 3px 0px 0px 40px;

    border: 0px 0px 0px;
  }

  div.table_of_contents {
    clear: left;

    min-width: 200px;

    margin: 3px 3px 3px 3px;

    background-color: #FFFFFF;

    text-align: left;
  }

  div.table_of_contents_item {
    clear: left;

    width: 100%;

    margin: 4px 0px 0px 0px;

    background-color: #FFFFFF;

    color: #000000;
    text-align: left;
  }

  div.table_of_contents_item a {
    margin: 6px 0px 0px 6px;
  }

  div.content_section {
    margin: 3px 3px 3px 3px;

    background-color: #FFFFFF;

    text-align: left;
  }

  div.content_section_text {
    padding: 4px 8px 4px 8px;

    color: #000000;
    font-size: 100%;
  }

  div.content_section_text pre {
    margin: 8px 0px 8px 0px;
    padding: 8px 8px 8px 8px;

    border-width: 1px;
    border-style: dotted;
    border-color: #000000;

    background-color: #F5F6F7;

    font-style: italic;
  }

  div.content_section_text p {
    margin-bottom: 6px;
  }

  div.content_section_text ul, div.content_section_text li {
    padding: 4px 8px 4px 16px;
  }

  div.section_header {
    padding: 3px 6px 3px 6px;

    background-color: #8E9CB2;

    color: #FFFFFF;
    font-weight: bold;
    font-size: 112%;
    text-align: center;
  }

  div.section_header_red {
    background-color: #CD214F;
  }

  div.section_header_grey {
    background-color: #9F9386;
  }

  .floating_element {
    position: relative;
    float: left;
  }

  div.table_of_contents_item a,
  div.content_section_text a {
    text-decoration: none;
    font-weight: bold;
  }

  div.table_of_contents_item a:link,
  div.table_of_contents_item a:visited,
  div.table_of_contents_item a:active {
    color: #000000;
  }

  div.table_of_contents_item a:hover {
    background-color: #000000;

    color: #FFFFFF;
  }

  div.content_section_text a:link,
  div.content_section_text a:visited,
   div.content_section_text a:active {
    background-color: #DCDFE6;

    color: #000000;
  }

  div.content_section_text a:hover {
    background-color: #000000;

    color: #DCDFE6;
  }

  div.validator {
  }
    </style>
  </head>
  <body>
    <div class="main_page">
      <div class="page_header floating_element">
        <img src="/icons/openlogo-75.png" alt="Debian Logo" class="floating_element"/>
        <span class="floating_element">
          Apache2 Debian Default Page
        </span>
      </div>
<!--      <div class="table_of_contents floating_element">
        <div class="section_header section_header_grey">
          TABLE OF CONTENTS
        </div>
        <div class="table_of_contents_item floating_element">
          <a href="#about">About</a>
        </div>
        <div class="table_of_contents_item floating_element">
          <a href="#changes">Changes</a>
        </div>
        <div class="table_of_contents_item floating_element">
          <a href="#scope">Scope</a>
        </div>
        <div class="table_of_contents_item floating_element">
          <a href="#files">Config files</a>
        </div>
      </div>
-->
      <div class="content_section floating_element">


        <div class="section_header section_header_red">
          <div id="about"></div>
          It works!
        </div>
        <div class="content_section_text">
          <p>
                This is the default welcome page used to test the correct 
                operation of the Apache2 server after installation on Debian systems.
                If you can read this page, it means that the Apache HTTP server installed at
                this site is working properly. You should <b>replace this file</b> (located at
                <tt>/var/www/html/index.html</tt>) before continuing to operate your HTTP server.
          </p>


          <p>
                If you are a normal user of this web site and don't know what this page is
                about, this probably means that the site is currently unavailable due to
                maintenance.
                If the problem persists, please contact the site's administrator.
          </p>

        </div>
        <div class="section_header">
          <div id="changes"></div>
                Configuration Overview
        </div>
        <div class="content_section_text">
          <p>
                Debian's Apache2 default configuration is different from the
                upstream default configuration, and split into several files optimized for
                interaction with Debian tools. The configuration system is
                <b>fully documented in
                /usr/share/doc/apache2/README.Debian.gz</b>. Refer to this for the full
                documentation. Documentation for the web server itself can be
                found by accessing the <a href="/manual">manual</a> if the <tt>apache2-doc</tt>
                package was installed on this server.

          </p>
          <p>
                The configuration layout for an Apache2 web server installation on Debian systems is as follows:
          </p>
          <pre>
/etc/apache2/
|-- apache2.conf
|       `--  ports.conf
|-- mods-enabled
|       |-- *.load
|       `-- *.conf
|-- conf-enabled
|       `-- *.conf
|-- sites-enabled
|       `-- *.conf
          </pre>
          <ul>
                        <li>
                           <tt>apache2.conf</tt> is the main configuration
                           file. It puts the pieces together by including all remaining configuration
                           files when starting up the web server.
                        </li>

                        <li>
                           <tt>ports.conf</tt> is always included from the
                           main configuration file. It is used to determine the listening ports for
                           incoming connections, and this file can be customized anytime.
                        </li>

                        <li>
                           Configuration files in the <tt>mods-enabled/</tt>,
                           <tt>conf-enabled/</tt> and <tt>sites-enabled/</tt> directories contain
                           particular configuration snippets which manage modules, global configuration
                           fragments, or virtual host configurations, respectively.
                        </li>

                        <li>
                           They are activated by symlinking available
                           configuration files from their respective
                           *-available/ counterparts. These should be managed
                           by using our helpers
                           <tt>
                                a2enmod,
                                a2dismod,
                           </tt>
                           <tt>
                                a2ensite,
                                a2dissite,
                            </tt>
                                and
                           <tt>
                                a2enconf,
                                a2disconf
                           </tt>. See their respective man pages for detailed information.
                        </li>

                        <li>
                           The binary is called apache2. Due to the use of
                           environment variables, in the default configuration, apache2 needs to be
                           started/stopped with <tt>/etc/init.d/apache2</tt> or <tt>apache2ctl</tt>.
                           <b>Calling <tt>/usr/bin/apache2</tt> directly will not work</b> with the
                           default configuration.
                        </li>
          </ul>
        </div>

        <div class="section_header">
            <div id="docroot"></div>
                Document Roots
        </div>

        <div class="content_section_text">
            <p>
                By default, Debian does not allow access through the web browser to
                <em>any</em> file apart of those located in <tt>/var/www</tt>,
                <a href="http://httpd.apache.org/docs/2.4/mod/mod_userdir.html" rel="nofollow">public_html</a>
                directories (when enabled) and <tt>/usr/share</tt> (for web
                applications). If your site is using a web document root
                located elsewhere (such as in <tt>/srv</tt>) you may need to whitelist your
                document root directory in <tt>/etc/apache2/apache2.conf</tt>.
            </p>
            <p>
                The default Debian document root is <tt>/var/www/html</tt>. You
                can make your own virtual hosts under /var/www. This is different
                to previous releases which provides better security out of the box.
            </p>
        </div>

        <div class="section_header">
          <div id="bugs"></div>
                Reporting Problems
        </div>
        <div class="content_section_text">
          <p>
                Please use the <tt>reportbug</tt> tool to report bugs in the
                Apache2 package with Debian. However, check <a
                href="http://bugs.debian.org/cgi-bin/pkgreport.cgi?ordering=normal;archive=0;src=apache2;repeatmerged=0"
                rel="nofollow">existing bug reports</a> before reporting a new bug.
          </p>
          <p>
                Please report bugs specific to modules (such as PHP and others)
                to respective packages, not to the web server itself.
          </p>
        </div>




      </div>
    </div>
    <div class="validator">
    </div>
  </body>
</html>

root@dev1-10:/home/demi/netol_do/devops-netology# 



```


9. Создайте скрипт, который будет генерировать новый сертификат в vault:
  - генерируем новый сертификат так, чтобы не переписывать конфиг nginx;
  - перезапускаем nginx для применения нового сертификата.


```bash



root@dev1-10:/home/demi/netol_do/devops-netology# cat vault/cert_man.sh
#!/bin/bash


crt_dir="/etc/ssl/certs"
key_dir="/etc/ssl/private"

renew() {


        domain_all=$1
        arrIN=(${domain_all//./ })
        domain2=${arrIN[-2]}.${arrIN[-1]}  
        echo $domain_all
        echo $domain2

        #create role
        vault write pki_int/roles/linkintel-dot-ru allowed_domains=$domain2 allow_subdomains=true max_ttl="720h"
        #request cert
        vault write pki_int/issue/linkintel-dot-ru common_name=$domain_all ttl="24h" | tee last_cert_key


        echo -e '\nImporting keys to /etc/ssl ...\n'












        cat last_cert_key | sed -z 's/\n/\|/g' last_cert_key | grep -o -E "certificate[ ]+[-]+BEGIN CERTIFICATE[-]+[\|](.)*[\|][-]+END CERTIFICATE[-]+[\|]expiration"  | sed -e "s/certificate         //g" | sed -e "s/[\|]expiration//g" | sed -e "y/\|/\n/" | tee /etc/ssl/certs/$domain_all.crt


        cat last_cert_key | sed ':a;N;$!ba;s/\n/ /g' last_cert_key | grep -o -E "[-]+BEGIN RSA PRIVATE KEY[-]+(.|\r\n|\n|$)*[-]+END RSA PRIVATE KEY[-]+" | sed 's/ /\n/g' | sed ':a;N;$!ba;s/RSA\n/RSA /g' | sed ':a;N;$!ba;s/PRIVATE\n/PRIVATE /g' | sed ':a;N;$!ba;s/BEGIN\n/BEGIN /g' | sed ':a;N;$!ba;s/END\n/END /g' | tee /etc/ssl/private/$domain_all.key


        #cat www.example.com.crt bundle.crt > www.example.com.chained.crt
        touch $crt_dir/$domain_all.chained.crt
        cat $crt_dir/$domain_all.crt > $crt_dir/$domain_all.chained.crt
        cat CA_cert_$domain_all.crt >> $crt_dir/$domain_all.chained.crt
        echo -e "\n" >> $crt_dir/$domain_all.chained.crt 
        cat intermediate.cert.$1.pem >> $crt_dir/$domain_all.chained.crt



}


new()  {

        export VAILT_ADDR='http://127.0.0.1:8200'
        export VAULT_TOKEN='root'

        #generate root cert authority
        cd /root/vault
        vault secrets enable pki
        vault secrets tune -max-lease-ttl=87600h pki
        vault write -field=certificate pki/root/generate/internal common_name="$1" ttl=87600h > CA_cert_$1.crt
        vault write pki/config/urls issuing_certificates="$VAULT_ADDR/v1/pki/ca" crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
        #generate intermediate ca
        vault secrets enable -path=pki_int pki
        vault secrets tune -max-lease-ttl=43800h pki_int
        vault write -format=json pki_int/intermediate/generate/internal common_name="$1 Intermediate Authority" | jq -r '.data.csr' > pki_intermediate.$1.csr
        vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.$1.csr format=pem_bundle ttl="43800h" | jq -r '.data.certificate' > intermediate.cert.$1.pem
        vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.$1.pem
        renew $1
}

restart() {
        pkill -9 vault
        echo "Use: 'vault server -dev -dev-root-token-id root' to start Vault server! Absent!"
}


revoke() {

        ser_num=$1
        echo $ser_num
        vault write pki_int/revoke serial_number=$ser_num

}

clean() {

        if [ `pgrep -f vault | wc -l` -gt 0 ];
        then
                echo -e "\nRemoving $1 certificate files ...\n"

                unset VAULT_ADDR VAULT_TOKEN

                `rm -f \
                CA_cert.$1.crt \
                intermediate.cert.$1.pem \
                pki_intermediate.$1.csr \
                payload.json \
                payload-url.json \
                payload-int.json \
                payload-int-cert.json \
                payload-signed.json \
                payload-role.json`

                pgrep -f vault | xargs kill
        else
                echo -e '\nNothing to clean!\n'
        fi
}



. /root/.bashrc

if [ $# -lt 2 ];
then
        echo -e "Please add cert domain name (f.e. 'test.example.com') as argument \$1 to exec script and action 'new'|'renew'|'revoke'|'clean'|'restart' as argument \$2 : \
                \n      new - generate root cert authority, \$1 - fqdn for certificate to create \
                \n      renew - create role & request certificate, \$1 - fqdn for renewed certificate & role \
                \n      revoke - revoke issued certificate, \$1 - serial number of RSA private key \
                \n      clean - remove expired certificates, no other arguments required \
                \n      restart - restart vault server. "
else
        if [  `netstat -lntp | grep vault | awk '{print $7}' | wc -l` -eq 0 ];
        then
                restart
        else

                if [ `vault status | grep Initialized | awk '{print $2}'` ];
                then

                        case $2 in
                        'new')
                                if [ `netstat -lntp | grep :8200 | awk '{print $7}' | wc -l` -gt 0 ];
                                then
                                        if [ `vault secrets list | grep pki | wc -l` -gt 0 ];
                                        then
                                                echo 'vault secrets pki already installed! use restart instead.'
                                        else
                                                new $1
                                        fi
                                else
                                        new $1
                                fi
                        ;;
                        'renew')
                                renew $1
                        ;;
                        'revoke')
                                revoke $1
                        ;;
                        'clean')
                                clean $1
                        ;;
                        'restart')

                                echo -e "\nMaking hard restart... Please check files & homedir!\n"
                                restart
                        ;;
                        esac

                else
                        restart
                fi
        fi
fi






```




10. Поместите скрипт в crontab, чтобы сертификат обновлялся какого-то числа каждого месяца в удобное для вас время.



```bash







root@dev1-10:~# crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
59 23 1 * * /root/vault/cert_man.sh test.linkintel.ru renew
root@dev1-10:~# 
```

> Скришот:




![Screenshot alt](/test.linkintel.ru3.png "Screenshot!")


```bash





https://drive.google.com/file/d/1DWQieoF3wntqnewOpkpEOixevCmns7QR/view?usp=sharing




```


## Результат

Результатом курсовой работы должны быть снимки экрана или текст:

- Процесс установки и настройки ufw
- Процесс установки и выпуска сертификата с помощью hashicorp vault
- Процесс установки и настройки сервера nginx
- Страница сервера nginx в браузере хоста не содержит предупреждений 
- Скрипт генерации нового сертификата работает (сертификат сервера ngnix должен быть "зеленым")
- Crontab работает (выберите число и время так, чтобы показать что crontab запускается и делает что надо)

## Как сдавать курсовую работу

Курсовую работу выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. 
Ссылка на инструкцию [Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop).
