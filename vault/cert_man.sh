#!/bin/bash
	
	
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









#	cat last_cert_key | sed ':a;N;$!ba; s/\n/ /g' last_cert_key | grep -o -E "certificate[ ]+[-]+BEGIN CERTIFICATE[-]+(.)* [-]+END CERTIFICATE[-]+ expiration" | sed -e "s/certificate         //g" | sed -e "s/ expiration//g" | sed -e "y/ /\n/" | tee /etc/ssl/certs/$domain_all.crt



	cat last_cert_key | sed -z 's/\n/\|/g' last_cert_key | grep -o -E "certificate[ ]+[-]+BEGIN CERTIFICATE[-]+[\|](.)*[\|][-]+END CERTIFICATE[-]+[\|]expiration"  | sed -e "s/certificate         //g" | sed -e "s/[\|]expiration//g" | sed -e "y/\|/\n/" | tee /etc/ssl/certs/$domain_all.crt


	cat last_cert_key | sed ':a;N;$!ba;s/\n/ /g' last_cert_key | grep -o -E "[-]+BEGIN RSA PRIVATE KEY[-]+(.|\r\n|\n|$)*[-]+END RSA PRIVATE KEY[-]+" | sed 's/ /\n/g' | sed ':a;N;$!ba;s/RSA\n/RSA /g' | sed ':a;N;$!ba;s/PRIVATE\n/PRIVATE /g' | sed ':a;N;$!ba;s/BEGIN\n/BEGIN /g' | sed ':a;N;$!ba;s/END\n/END /g' | tee /etc/ssl/private/$domain_all.key


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
	vault write -format=json pki_int/intermediate/generate/internal common_name="test.$1 Intermediate Authority" | jq -r '.data.csr' > pki_intermediate.$1.csr
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
		\n	new - generate root cert authority, \$1 - fqdn for certificate to create \
		\n	renew - create role & request certificate, \$1 - fqdn for renewed certificate & role \
		\n	revoke - revoke issued certificate, \$1 - serial number of RSA private key \
		\n	clean - remove expired certificates, no other arguments required \
		\n	restart - restart vault server. "
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

				echo -e "\nMaking hard restar... Please check files & homedir!\n"
				restart
			;;
			esac

		else
			restart
		fi
	fi
fi
