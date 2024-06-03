class Repository:
    def __init__(self, class1):
        self.class1 = class1

    # 新增物件
    def create(self, **dict1):
        obj = self.class1()
        for key in dict1.keys():
            setattr(obj, key, dict1[key])
        obj.save()
        return obj

    # 多筆新增
    def bulkCreate(self, objs):
        return self.class1.objects.bulk_create(objs)

    # 存檔(新增或更新)
    def save(self, obj):
        return obj.save()

    # 刪除 By Id
    def deleteById(self, pk):
        return self.class1.objects.filter(pk=pk).delete()

    # 刪除 By 物件
    def deleteObject(self, obj):
        return obj.delete()

    # 單筆查詢
    def getById(self, pk):
        return self.class1.objects.get(pk=pk)

    # 多筆查詢
    def findAll(self, **filter):
        return self.class1.objects.filter(**filter)
