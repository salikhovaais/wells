from clientW import GetWitsml, DeleteWitsml, PostPutWitsml

Get = GetWitsml()
xml_wells = Get.get_inform()
print(xml_wells)
# # for i in xml_wells:
# #     print(xml_wells)