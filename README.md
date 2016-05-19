### INSTALL

pip install git+https://github.com/astwyg/ct-rest.git


### USE

```python
#at view.py
@REST(method="GET",
      header=["crm_id"])
def testdb(request):
    accounts = AccountCrm.objects.all()
    que = Q(crm_id = "01cb72f9e07a4cbc813880efde8afd89") | Q(crm_id="035c243ebf12483eb498c9d8295cc476") | Q(crm_id__contains="00")
    accounts = AccountCrm.objects.filter(que)
    result = []
    for ins in accounts:
        result.append(ins.crm_id+"\n")
    return result
```