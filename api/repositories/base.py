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
    def bulk_create(self, objs):
        return self.class1.objects.bulk_create(objs)

    # 存檔(新增或更新)
    def save(self, obj):
        return obj.save()

    # 刪除 By Id
    def delete_by_id(self, pk):
        return self.class1.objects.filter(pk=pk).delete()

    # 刪除 By 物件
    def delete_object(self, obj):
        return obj.delete()

    # 單筆查詢
    def get_by_id(self, pk):
        return self.class1.objects.get(pk=pk)

    # 多筆查詢
    def find_all(self, **filter):
        return self.class1.objects.filter(**filter)
