# brand-model2name
This is a simple package that takes a brand name as input and returns the corresponding model name.

Rely on [KHwang9883's MobileModels](https://github.com/KHwang9883/MobileModels)

## Installation
```shell
$ pip install brand-model2name
```

## Example
Model2Name init need 2 parameters:
1. brands:

    A list of brand names, can choose any brand name in the list which includes 'samsung', 'oneplus', 'apple', 'zte', 'honor', 'huawei', 'google', '360shouji', 'mitv', 'oppo', 'blackshark', 'meizu', 'nubia', 'vivo', 'sony', 'coolpad', 'smartisan', 'xiaomi', 'asus', 'nokia', 'lenovo', 'zhixuan', 'motorola', 'nothing', 'realme', 'letv'.
    
    The default value is set to all of the above brands

2. device:

    Can choose any one from 'mobile', 'tv', 'wearable' and 'all'.

    The default value is set 'mobile'.

📔: Suggest to use a singleton object to use.
```python
from model2name import Model2Name

m2n = Model2Name()
print(m2n.get_model_name("A1324"))
# Output:
# {"brand": "苹果", "model": "iPhone 3G (China mainland)"}
print(m2n.get_model_name("unknown-model"))
# Output:
# {}

# if you init just like this, it only has 'xiaomi' and 'apple' brands and their TV models.
m2n = Model2Name(device='tv', brands=['xiaomi', 'apple'])
```


---
GitHub Actions are supported and automatically updated daily. Please add GITHUB_TOKEN after Fork or PR, refer to[GitHub Token](https://docs.github.com/cn/actions/security-guides/automatic-token-authentication)
