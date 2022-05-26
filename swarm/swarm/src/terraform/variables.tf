# Заменить на ID своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_cloud_id" {
  default = "b1gtlo6uqrvrdckscbg8"
}

# Заменить на Folder своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_folder_id" {
  default = "b1g7jkg3844vv1nn5r1a"
}

# Заменить на ID своего образа
# ID можно узнать с помощью команды yc compute image list
variable "centos-7-base" {
  default = "fd8dib4t4ekaijvk09rp"
}

variable "ssh_user"  {
  type = string
  default = "centos"
}





variable "ssh_keys" {
  type = list(object({
    publickey = string
    user = string
  }))
  description = "list of public ssh keys that have access to the VM"
  default = [
/*
      {
        user = "centos"
        publickey = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/EBW4EvwnnNwWdOQ1j6YIOWB3vva9eirTQVKrRCytfctp9ywoprD4HyLUAY5nWwlepkD3JtMDQEsuPEZpm6ehqOX5oteK4NZ8Jp6aPwQLIyK5g2QetxJxnEHMpXW2nymnNBAen/2tX2c65rAVn0k7sDAY34+IerZaVKU1PKF2DjkK845CZRbYoIOnCjPZVGu4uIzlPMTPgPWTMP4qjIuq3kgnJsOBpTRIf7OpDKSKXKuKRfE/eILlBONPpRtFxkLZwmBw1B3KsNjbeAguIbkMgOoUmdzvxffcPR0Wsu0me52NQJ4srgVL5QTXGgUSLgoTv1L30fFi0jqFVwZVTCWF root@dev1"
      }, 
*/
      {
        user = "centos"
        publickey = "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEApyD2VIlftoGyH5wLuwxP3Lwufc17zKaW3f1xf0Q9i2N/bMyv5hc61F5FMmaho4s8Xa9Clvaiv+mcwi6Nzk7SST/tqoVPr6OsegyqcMFcnKj8Tt9LXYYwHqFSJ3fF8u/qNtdZ4W2rUDwTYnZDs6LFvOYxhh/F1Y0lahmfkS+oedhqPLI7/WWq7A/RdcwyfQwOoSN+Avqiyj1B6+Snk22LpcF9vJ1HVR28X7mYkhG9G0jke+32Wt/wf18QTG79YGdjZW+qFA9RxjUolR81DioL7kBTPUWqyqPtZiNrBirJ8jPYnRwtGg4nhq2km/sWXF59xSg0yysazvGaRsWnTGMb5w== demi@adminpc"
      }
  ]
}



variable "ssh_key_dev1-10" {
  type = string
  default = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/EBW4EvwnnNwWdOQ1j6YIOWB3vva9eirTQVKrRCytfctp9ywoprD4HyLUAY5nWwlepkD3JtMDQEsuPEZpm6ehqOX5oteK4NZ8Jp6aPwQLIyK5g2QetxJxnEHMpXW2nymnNBAen/2tX2c65rAVn0k7sDAY34+IerZaVKU1PKF2DjkK845CZRbYoIOnCjPZVGu4uIzlPMTPgPWTMP4qjIuq3kgnJsOBpTRIf7OpDKSKXKuKRfE/eILlBONPpRtFxkLZwmBw1B3KsNjbeAguIbkMgOoUmdzvxffcPR0Wsu0me52NQJ4srgVL5QTXGgUSLgoTv1L30fFi0jqFVwZVTCWF root@dev1"
}

variable "ssh_key_demizen" {
  type = string
  default = "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEApyD2VIlftoGyH5wLuwxP3Lwufc17zKaW3f1xf0Q9i2N/bMyv5hc61F5FMmaho4s8Xa9Clvaiv+mcwi6Nzk7SST/tqoVPr6OsegyqcMFcnKj8Tt9LXYYwHqFSJ3fF8u/qNtdZ4W2rUDwTYnZDs6LFvOYxhh/F1Y0lahmfkS+oedhqPLI7/WWq7A/RdcwyfQwOoSN+Avqiyj1B6+Snk22LpcF9vJ1HVR28X7mYkhG9G0jke+32Wt/wf18QTG79YGdjZW+qFA9RxjUolR81DioL7kBTPUWqyqPtZiNrBirJ8jPYnRwtGg4nhq2km/sWXF59xSg0yysazvGaRsWnTGMb5w== demi@adminpc"
}
