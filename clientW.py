import io

from komle.bindings.v1411.read import witsml
from komle.soap_client import StoreClient, _parse_reply

ver = f'version="{witsml.__version__}"'
ver_xmlns = f'version="{witsml.__version__}" xmlns="http://www.witsml.org/schemas/1series"'


class GetWitsml():

    def __init__(self, service_url = 'http://10.23.125.144/Witsml.Web/api/soap', username = 'navigator',
                 password ='Qwe123!!!'):
        self._server = StoreClient(service_url=service_url,
                                   username=username,
                                   password=password)
        self._obj_func = {"well": self._soap_wells,
                          "log": self._soap_logs,
                          "trajectory": self._soap_trajectorys,
                          "wellbore": self._soap_wellbores}

    def _soap_data(self, xml=witsml.wells(version=witsml.__version__).append(witsml.obj_well()).toxml(),
                   type_data="well"):
        return self._server.soap_client.service.WMLS_GetFromStore(type_data,
                                                                  xml.replace(ver, ver_xmlns),
                                                                  OptionsIn=f'returnElements=all')
        # return self.server.soap_client.service.WMLS_GetFromStore(type_data,
        #                                                                       xml.replace(ver, ver_xmlns),
        #                                                                       OptionsIn=f'returnElements=all')

    def _soap_wells(self, uid=None, uid_well=None, uid_wellbore=None):
        xml = witsml.wells(version=witsml.__version__).append(witsml.obj_well(uid=uid)).toxml()
        return self._soap_data(xml=xml)

    def _soap_logs(self, uid=None, uid_well=None, uid_wellbore=None):
        xml = witsml.logs(version=witsml.__version__).append(witsml.obj_log(uid=uid,
                                                                            uidWell=uid_well,
                                                                            uidWellbore=uid_wellbore)).toxml()
        return self._soap_data(xml=xml,
                               type_data="log")

    def _soap_trajectorys(self, uid=None, uid_well=None, uid_wellbore=None):
        xml = witsml.trajectorys(version=witsml.__version__).append(witsml.obj_trajectory(uid=uid,
                                                                                          uidWell=uid_well,
                                                                                          uidWellbore=uid_wellbore)).toxml()
        return self._soap_data(xml=xml,
                               type_data="trajectory")

    def _soap_wellbores(self, uid=None, uid_well=None, uid_wellbore=None):
        xml = witsml.wellbores(version=witsml.__version__).append(witsml.obj_wellbore(uid=uid,
                                                                                      uidWell=uid_well)).toxml()
        return self._soap_data(xml=xml,
                               type_data="wellbore")

    def get_inform(self, xml=False, type="well", uid=None, uid_well=None, uid_wellbore=None):
        data = self._obj_func[type](uid=uid, uid_well=uid_well, uid_wellbore=uid_wellbore)
        if xml:
            return data.XMLout
        else:
            return self._get_inform_list(_parse_reply(data), type)

    def is_exist(self, type="well", uid=None, uid_well=None, uid_wellbore=None):
        data = self.get_inform(type, uid, uid_well, uid_wellbore)
        if len(data) == 0:
            return False
        else:
            return data

    def _get_uids(self, obj, obj_dict):
        attr = {}
        for key in ["uidWell", "uidWellbore", "uid"]:
            try:
                attr.update({key: getattr(obj, key)})
            except:
                pass
        obj_dict.update({"attr": attr})

    def _get_inform_list(self, data, type):
        objs = getattr(data, type)
        ret_list = []
        for obj in objs:
            obj_dict = {}
            self._get_uids(obj, obj_dict)
            # ret_dict = obj.uid

            self._main_inform(obj.toDOM(None, element_name=None).documentElement.childNodes, obj_dict)
            ret_list.append(obj_dict)
        return ret_list

    def _get_list_elem(self, data, old):
        try:
            return old + [data]
        except:
            return [old, data]

    def _unique_value(self, dict_data, data, key_field):
        if key_field in dict_data:
            # print(dict_data[ch.localName])
            return {key_field: self._get_list_elem(data, dict_data[key_field])}
        else:
            return {key_field: data}

    def _get_params(self, attributes, data):
        attr_dict = {}
        for attr in attributes.keys():
            attr_dict.update({attr: attributes[attr].value})
        data.update({"attr": attr_dict})

    def _field_value(self, ch):
        if len(ch._get_attributes().keys()) == 0:
            return ch.firstChild.data
        else:
            data = {"value": ch.firstChild.data}
            self._get_params(ch._get_attributes(), data)
            return data

    def _get_childs(self, ch):
        data = {}
        self._get_params(ch._get_attributes(), data)
        self._main_inform(ch.childNodes, data)
        return data

    def _main_inform(self, objs, dict_data):
        for ch in objs:
            try:
                data = self._field_value(ch)
            except:
                data = self._get_childs(ch)

            dict_data.update(self._unique_value(dict_data, data, ch.localName))


class DeleteWitsml():
    def __init__(self,service_url = 'http://10.23.125.144/Witsml.Web/api/soap', username = 'navigator',
                 password ='Qwe123!!!'):
        self._server = StoreClient(service_url=service_url,
                                   username=username,
                                   password=password)
        self._obj_func = {"well": self._delete_wells,
                          "log": self._delete_logs,
                          "trajectory": self._delete_trajectorys,
                          "wellbore": self._delete_wellbores}

    def _get_options(self, cascade=False):
        return f'returnElements=all;cascadedDelete={cascade}'

    def _soap_delete(self, xml=None, type_data="well", cascade=False):
        if xml:
            return self._server.soap_client.service.WMLS_DeleteFromStore(type_data,
                                                                         xml.replace(ver, ver_xmlns),
                                                                         OptionsIn=self._get_options(cascade))
        else:
            return None

    def _delete_wells(self, uid=None, uid_well=None, uid_wellbore=None, cascade=False):
        if uid:
            xml = witsml.wells(version=witsml.__version__).append(witsml.obj_well(uid=uid)).toxml()
            return self._soap_delete(xml=xml, cascade=cascade)
        else:
            return None

    def _delete_logs(self, uid=None, uid_well=None, uid_wellbore=None, cascade=False):
        if uid and uid_well and uid_wellbore:
            xml = witsml.logs(version=witsml.__version__).append(witsml.obj_log(uidWell=uid_well,
                                                                                uidWellbore=uid_wellbore,
                                                                                uid=uid)).toxml()
            return self._soap_delete(xml=xml,
                                     type_data="log", cascade=cascade)
        else:
            return None

    def _delete_trajectorys(self, uid=None, uid_well=None, uid_wellbore=None, cascade=False):
        if uid and uid_well and uid_wellbore:
            xml = witsml.trajectorys(version=witsml.__version__).append(witsml.obj_trajectory(uidWell=uid_well,
                                                                                              uidWellbore=uid_wellbore,
                                                                                              uid=uid)).toxml()
            return self._soap_delete(xml=xml,
                                     type_data="trajectory", cascade=cascade)
        else:
            return None

    def _delete_wellbores(self, uid=None, uid_well=None, uid_wellbore=None, cascade=False):
        if uid and uid_well:
            xml = witsml.wellbores(version=witsml.__version__).append(witsml.obj_wellbore(uidWell=uid_well,
                                                                                          uid=uid)).toxml()
            return self._soap_delete(xml=xml,
                                     type_data="wellbore", cascade=cascade)
        else:
            return None

    def _get_result(self, data):
        if data:
            if data.Result == 1:
                return "Success"
            else:
                return data.SuppMsgOut
        else:
            return "The input template must specify the unique identifiers of one data-object to be processed. Error " \
                   "Code: -415 "

    def delete_inform(self, type="well", uid=None, uid_well=None, uid_wellbore=None, cascade=False):
        data = self._obj_func[type](uid=uid, uid_well=uid_well, uid_wellbore=uid_wellbore, cascade=cascade)
        return self._get_result(data)


class PostPutWitsml():
    def __init__(self,service_url = 'http://10.23.125.144/Witsml.Web/api/soap', username = 'navigator',
                 password ='Qwe123!!!'):
        self._server = StoreClient(service_url=service_url,
                                   username=username,
                                   password=password)
        self._def_uids = {"well": ["uid"],
                          "wellbore": ["uid", "uidWell"],
                          "trajectory": ["uid", "uidWell", "uidWellbore"],
                          "log": ["uid", "uidWell", "uidWellbore"]}

    def _soap_post(self, xml=None, type_data="well"):
        if xml:
            return self._server.soap_client.service.WMLS_AddToStore(type_data,
                                                                    xml,
                                                                    OptionsIn=f'returnElements=all')
        else:
            return None

    def _soap_put(self, xml=None, type_data="well"):
        if xml:
            return self._server.soap_client.service.WMLS_UpdateInStore(type_data,
                                                                       xml,
                                                                       OptionsIn=f'returnElements=all')
        else:
            return None

    def _get_result(self, data):
        if data:
            return data.SuppMsgOut

    def post_inform(self, xml=None, path=None, data=None, type_data="well", version="1.4.1.1"):
        return self._get_result(self._soap_post(self._get_xml(xml, path, data, type_data, version), type_data))

    def put_inform(self, xml=None, path=None, data=None, type_data="well", version="1.4.1.1"):
        result = self._soap_put(self._get_xml(xml, path, data, type_data, version), type_data)
        if result.Result == 1:
            return "Success"
        else:
            return self._get_result(result)

    def _get_xml(self, xml=None, path=None, data=None, type_data="well", version="1.4.1.1"):
        if path:
            try:
                with open(path, 'r') as file:
                    xml = file.read()
            except BaseException as e:
                raise Exception(e)
        if data:
            xml = self._writexml(data, type_data, version)
        return xml

    def _get_uid(self, data, attr):
        try:
            return f' {attr}="{data[attr]}"'
        except KeyError:
            return ""

    def _check_attr(self, data, exc=True):
        try:
            attr = data["attr"]
            return attr
        except:
            if exc:
                raise Exception('Missing element "attr"')
            else:
                return None

    def _get_uids(self, data, type_el):
        if data and self._check_uids_type(type_el, data) == True:
            return f'<{type_el}{self._get_uid(data, "uidWell")}' \
                   f'{self._get_uid(data, "uidWellbore")}{self._get_uid(data, "uid")}>\n'
        else:
            return None

    def _check_uids_type(self, type_el, data):
        for key in self._def_uids[type_el]:
            if key not in data:
                raise Exception(f'Missing element in "attr" {key}')
        return True

    def _get_writer(self, type_el, version):
        writer = io.StringIO()
        writer.write('<?xml version="1.0" ?>')
        writer.write(f'<{type_el}s xmlns="http://www.witsml.org/schemas/1series" version="{version}">\n')
        return writer

    def _write_uids(self, writer, uids, data):
        writer.write(uids)
        del data["attr"]

    def _write_els(self, writer, data):
        for key in data.keys():
            self._wr_elem(writer, data[key], key)

    def _write_end_type(self, type_el, writer):
        writer.write(f'</{type_el}>\n</{type_el}s>')

    def _writexml(self, data, type_el="well", version="1.4.1.1"):
        uids = self._get_uids(self._check_attr(data), type_el)
        if uids:
            writer = self._get_writer(type_el, version)

            self._write_uids(writer, uids, data)
            self._write_els(writer, data)
            self._write_end_type(type_el, writer)

            return writer.getvalue()
        else:
            return None

    def _get_attr_el(self, writer, data, key):
        writer.write(f"<{key}")

        attrs = self._check_attr(data, False)
        if attrs:
            for atr in attrs.keys():
                writer.write(f' {atr}="{attrs[atr]}"')
            del data["attr"]
        writer.write(">")

    def _wr_list_el(self, writer, data, key):
        for element in data:
            self._wr_elem(writer, element, key)

    def _wr_pref(self, writer, data, key):
        if key not in ["value", "attr"] and type(data) != list:
            self._get_attr_el(writer, data, key)

    def _wr_postf(self, writer, type, key):
        if key not in ["value", "attr"] and type != list:
            writer.write(f"</{key}>\n")

    def _wr_dict_el(self, writer, data):
        for key_el in data.keys():
            self._wr_elem(writer, data[key_el], key_el)

    def _wr_elem(self, writer, data, key):
        if type(data) == list:
            self._wr_list_el(writer, data, key)
        self._wr_pref(writer, data, key)
        if type(data) == dict:
            self._wr_dict_el(writer, data)
        elif type(data) != list:
            writer.write(f'{data}')
        self._wr_postf(writer, type(data), key)
