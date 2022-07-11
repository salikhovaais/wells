from clientW import GetWitsml, DeleteWitsml, PostPutWitsml

# пример xml
xml = '<?xml version="1.0"?><wells version="1.4.1.1"' \
      'xmlns="http://www.witsml.org/schemas/1series"><well uid="w-12"><name>TEST1</name>' \
      '<nameLegal>Company Legal Name</nameLegal><numLicense>Company License Number</numLicense>' \
      '<numGovt>Govt-Number</numGovt><dTimLicense>2001-05-15T13:20:00.0000000+00:00</dTimLicense>' \
      '<country>US</country><state>TX</state><timeZone>-06:00</timeZone>' \
      '<dTimSpud>2001-05-31T08:15:00.0000000+00:00</dTimSpud><dTimPa>2001-07-15T15:30:00.0000000+00:00</dTimPa>' \
      '<wellheadElevation uom="ft">500</wellheadElevation><wellDatum uid="KB"><name>Kelly Bushing</name>' \
      '<code>KB</code><elevation uom="ft" datum="SL">78.5</elevation></wellDatum><wellDatum uid="SL">' \
      '<name>Sea Level</name><code>SL</code></wellDatum><groundElevation uom="ft">250</groundElevation>' \
      '<waterDepth uom="ft">520</waterDepth><wellLocation uid="loc-1"><wellCRS uidRef="proj1">ED50 / UTM Zone 31N' \
      '</wellCRS><easting uom="m">425353.84</easting><northing uom="m">6623785.69</northing>' \
      '<description>Location of well surface point in projected system.</description></wellLocation>' \
      '<referencePoint uid="SRP1"><name>Slot Bay Centre</name><type>Site Reference Point</type>' \
      '<location uid="loc-1"><wellCRS uidRef="proj1">ED50 / UTM Zone 31N</wellCRS>' \
      '<easting uom="m">425366.47</easting><northing uom="m">6623781.95</northing></location>' \
      '<location uid="loc-2"><wellCRS uidRef="localWell1">WellOneWSP</wellCRS>' \
      '<localX uom="m">12.63</localX><localY uom="m">-3.74</localY>' \
      '<description>Location of the Site Reference Point with respect to the well surface point</description>' \
      '</location></referencePoint><referencePoint uid="WRP2"><name>Sea Bed</name>' \
      '<type>Well Reference Point</type><elevation uom="ft" datum="SL">-118.4</elevation>' \
      '<measuredDepth uom="ft" datum="KB">173.09</measuredDepth><location uid="loc-1">' \
      '<wellCRS uidRef="proj1">ED50 / UTM Zone 31N</wellCRS><easting uom="m">425353.84</easting>' \
      '<northing uom="m">6623785.69</northing></location><location uid="loc-2">' \
      '<wellCRS uidRef="geog1">ED50</wellCRS><latitude uom="dega">59.743844</latitude>' \
      '<longitude uom="dega">1.67198083</longitude></location></referencePoint><wellCRS uid="geog1">' \
      '<name>ED50</name><geodeticCRS uidRef="4230">4230</geodeticCRS>' \
      '<description>ED50 system with EPSG code 4230.</description></wellCRS><wellCRS uid="proj1">' \
      '<name>ED50 / UTM Zone 31N</name><mapProjectionCRS uidRef="23031">ED50 / UTM Zone 31N</mapProjectionCRS>' \
      '</wellCRS><wellCRS uid="localWell1"><name>WellOneWSP</name><localCRS>' \
      '<usesWellAsOrigin>true</usesWellAsOrigin><yAxisAzimuth uom="dega" northDirection="grid north">0' \
      '</yAxisAzimuth><xRotationCounterClockwise>false</xRotationCounterClockwise></localCRS>' \
      '</wellCRS><commonData><dTimCreation>2022-07-08T14:20:52.5559688+00:00</dTimCreation>' \
      '<dTimLastChange>2022-07-08T14:20:52.5559688+00:00</dTimLastChange><itemState>plan</itemState>' \
      '<comments>These are the comments associated with the Well data object.</comments></commonData></well></wells>'

# пример словаря для создания/обновления данных
# uid, uom, datum, uidRef, northDirection и прочие атрибуты выносятся в словарь с ключем 'attr'
# в случае, когда есть простое значение и атрибуты, значение выносится в ключ 'value'
# например, <groundElevation uom="ft">250</groundElevation> примет вид
# 'groundElevation':
#              {'value': '250',
#               'attr': {'uom': 'ft'}}
# в случае множества элементов одного типа, они записываются в list
# в случае множества элементов разного типа, они записывают в dict с ключами - названиями их типов
# например, <wellDatum uid="KB">
#               <name>Kelly Bushing</name>
#               <code>KB</code>
#               <elevation uom="ft" datum="SL">78.5</elevation>
#           </wellDatum>
#           <wellDatum uid="SL">
#               <name>Sea Level</name>
#               <code>SL</code>
#           </wellDatum>
# примет вид:
# 'wellDatum': [
#              {
#                  'attr': {'uid': 'KB'},
#                  'name': 'Kelly Bushing',
#                  'code': 'KB',
#                  'elevation': {'value': '78.5', 'attr': {'uom': 'ft', 'datum': 'SL'}}
#              },
#              {
#                  'attr': {'uid': 'SL'},
#                  'name': 'Sea Level',
#                  'code': 'SL'
#              }]
data = {'attr': {'uid': 'w-12'},
         'name': 'ED50',
         'nameLegal': 'Company Legal Name',
         'numLicense': 'Company License Number',
         'numGovt': 'Govt-Number',
         'dTimLicense': '2001-05-15T13:20:00Z',
         'country': 'US',
         'state': 'TX',
         'timeZone': '-06:00',
         'dTimSpud': '2001-05-31T08:15:00Z',
         'dTimPa': '2001-07-15T15:30:00Z',
         'wellheadElevation':
             {'value': '500.0',
              'attr': {'uom': 'ft'}},
         'wellDatum': [
             {
                 'attr': {'uid': 'KB'},
                 'name': 'Kelly Bushing',
                 'code': 'KB',
                 'elevation': {'value': '78.5', 'attr': {'uom': 'ft', 'datum': 'SL'}}
             },
             {
                 'attr': {'uid': 'SL'},
                 'name': 'Sea Level', 'code': 'SL'
             }],
         'groundElevation': {'value': '250.0', 'attr': {'uom': 'ft'}},
         'waterDepth': {'value': '520.0', 'attr': {'uom': 'ft'}},
         'wellLocation': {'attr': {'uid': 'loc-1'},
                          'wellCRS': {
                              'value': 'ED50 / UTM Zone 31N',
                              'attr': {'uidRef': 'proj1'}},
                          'easting': {'value': '425353.84',
                                      'attr': {'uom': 'm'}},
                          'northing': {'value': '6623785.69',
                                       'attr': {'uom': 'm'}},
                          'description': 'Location of well surface point in projected system.'},
         'referencePoint': [
             {'attr': {'uid': 'SRP1'},
              'name': 'Slot Bay Centre', 'type': 'Site Reference Point',
              'location': [{'attr': {'uid': 'loc-1'},
                            'wellCRS': {'value': 'ED50 / UTM Zone 31N', 'attr': {'uidRef': 'proj1'}},
                            'easting': {'value': '425366.47', 'attr': {'uom': 'm'}},
                            'northing': {'value': '6623781.95', 'attr': {'uom': 'm'}}},
                           {'attr': {'uid': 'loc-2'},
                            'wellCRS': {'value': 'WellOneWSP', 'attr': {'uidRef': 'localWell1'}},
                            'localX': {'value': '12.63', 'attr': {'uom': 'm'}},
                            'localY': {'value': '-3.74', 'attr': {'uom': 'm'}},
                            'description': 'Location of the Site Reference Point with respect to the well surface point'}]},
             {'attr': {'uid': 'WRP2'}, 'name': 'Sea Bed', 'type': 'Well Reference Point',
              'elevation': {'value': '-118.4', 'attr': {'uom': 'ft', 'datum': 'SL'}},
              'measuredDepth': {'value': '173.09', 'attr': {'uom': 'ft', 'datum': 'KB'}},
              'location': [{'attr': {'uid': 'loc-1'},
                            'wellCRS': {'value': 'ED50 / UTM Zone 31N', 'attr': {'uidRef': 'proj1'}},
                            'easting': {'value': '425353.84', 'attr': {'uom': 'm'}},
                            'northing': {'value': '6623785.69', 'attr': {'uom': 'm'}}},
                           {'attr': {'uid': 'loc-2'}, 'wellCRS': {'value': 'ED50', 'attr': {'uidRef': 'geog1'}},
                            'latitude': {'value': '59.743844', 'attr': {'uom': 'dega'}},
                            'longitude': {'value': '1.67198083', 'attr': {'uom': 'dega'}}}]}],
         'wellCRS': [{'attr': {'uid': 'geog1'}, 'name': 'ED50',
                      'geodeticCRS': {'value': '4230', 'attr': {'uidRef': '4230'}},
                      'description': 'ED50 system with EPSG code 4230.'}, {'attr': {'uid': 'proj1'},
                                                                           'name': 'ED50 / UTM Zone 31N',
                                                                           'mapProjectionCRS': {'value': 'ED50 / UTM Zone 31N',
                                                                                                'attr': {'uidRef': '23031'}}},
                     {'attr': {'uid': 'localWell1'}, 'name': 'WellOneWSP',
                      'localCRS': {'attr': {}, 'usesWellAsOrigin': 'true',
                                   'yAxisAzimuth': {'value': '0.0',
                                   'attr': {'uom': 'dega',
                                            'northDirection': 'grid north'}},
                                   'xRotationCounterClockwise': 'false'}}],
         'commonData': {'attr': {}, 'dTimCreation': '2022-07-08T16:54:40.345403Z',
                        'dTimLastChange': '2022-07-08T16:59:39.538102Z', 'itemState': 'plan',
                        'comments': 'These are the comments associated with the Well data object.'}}


# Класс для получения информации, в котором с помощью функции get_inform() можно получить информацию
# по "well", "log", "trajectory" и "wellbore".
Get = GetWitsml()

# функция get_inform(xml=False, type="well", uid=None, uid_well=None, uid_wellbore=None)
# параметр xml:
# если True возвращает XMLout ответа (стандартное soap-сообщение) с информацией об объектах,
# если False возвращает список со словарями объектов (так далее по объектам в зависимости от конфигурации) list<dict>
# параметр type:
# данные, которые следует получить: "well", "log", "trajectory" или "wellbore"
# параметр uid: uid объекта (у всех объектов)
# параметр uid_well: uid скважины (для "log", "trajectory" и "wellbore")
# параметр uid_wellbore: uid ствола (для "log" и "trajectory")
# параметры uid, uid_well и uid_wellbore могут не задаваться
# (в зависимости от их наличия меняется набор возвращаемых данных)
xml_wells = Get.get_inform(type="well", uid="w-12", xml=True)
wells = Get.get_inform(type="well", uid="w-12")

# -----------------------------------#
# Класс для удаления информации, в котором с помощью функции delete_inform() можно удалить информацию
# по "well", "log", "trajectory" и "wellbore".
Delete = DeleteWitsml()

# функция delete_inform(type="well", uid=None, uid_well=None, uid_wellbore=None, cascade=False))
# параметр type:
# данные, которые следует удалить: "well", "log", "trajectory" или "wellbore"
# параметр uid: uid объекта (у всех объектов)
# параметр uid_well: uid скважины (для "log", "trajectory" и "wellbore")
# параметр uid_wellbore: uid ствола (для "log" и "trajectory")
# параметры uid, uid_well и uid_wellbore обязательны в тех объектах, в которых определены!
# параметр cascade:
# если True возможно удаления объекта вместе со всеми дочерними объектами
# (при удалении скважены удаляться существующие ее "log", "trajectory" и "wellbore")
# если False, невозможно удалить объект, у которого существуют дочерние объекты
Delete.delete_inform(type="well", uid="w-12")

# -----------------------------------#
# Класс для создания/обновления информации, в котором с помощью функций post_inform()/put_inform()
# можно создавать/обновлять информацию
# по "well", "log", "trajectory" и "wellbore".
Post = PostPutWitsml()


# функции post_inform/put_inform(xml=None, path=None, data=None, type_data="well"))
# параметр xml:
# в данный параметр можно задавать xml-сообщение(пример в начале xml), которое будет отправлено для создания объекта
# параметр path:
# в данный параметр можно задавать путь к xml-файлу, в котором расположены xml-данные,
# которые будут отправлены для создания объекта
# параметр data:
# в данный параметр можно задавать словарь с данными(пример в начале data), который будет отправлен для создания объекта
# параметр type_data:
# данные, которые следует удалить: "well", "log", "trajectory" или "wellbore"



# Важно при создании! наличие в отправляемых данных uid: uid объекта (у всех объектов),
# uidWell: uid скважины (для "log", "trajectory" и "wellbore")
# uidWellbore: uid ствола (для "log" и "trajectory")
# uid, uidWell и uidWellbore обязательны в тех объектах, в которых определены!
# в словаре они задаются в attr главного словаря с ключами uid, uidWell и uidWellbore

Post.post_inform(data=data)
Post.post_inform(xml=xml)


Post.put_inform(data=data)
Post.put_inform(xml=xml)

