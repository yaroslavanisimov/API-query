from win32comext.axscript.server.error import Exception

from dbmodule import session, Task


class dao(object):
    def __init__(self):
        pass

    def create(self, obj):
        """Storage class instance to database
                  : Param Obj specific class instance
                  : return no"""
        session.add(obj)
        session.commit()

    def update(self, obj):
        """
                    Update data, query data in the database according to OBJ's ID
                    If OBJ uses session queries, and with Update uses the same session, there is no change in the middle of the change that it will not be executed, and the data in the session has been modified directly to Commital
                    If OBJ is just reserved id, one instance of self-definition is not queried in the same session, all attributes in the traversal instance (attribute non-_-outfit) cycle will generate inconsistent data,
                    Use SetAttr to modify and update, and call the commit to finally submit, so this of this commission must be executed.
                    : PARAM OBJ modified instance
                    : raise entryNotFoundException does not reach an instance
                    : Raise ObjectNotmatChexception Obj and database query class is not the same type
                    : return no
       """
        if isinstance(obj, self.get_entityclass()):
            try:
                obj_saved = self.find_by_id(obj.id)
                if obj_saved is None:
                    raise EntryNotFoundException()
                for attribute_name in dir(obj_saved):
                    if attribute_name[0:1] != "_" and \
                            getattr(obj, attribute_name) != getattr(obj_saved, attribute_name):
                        setattr(obj_saved, attribute_name, getattr(obj, attribute_name))
                self.__commit()
            except Exception as e:
                raise e
            else:
                raise ObjectNotMatchException()


    def __commit(self):
        session.commit()

    def get_entityclass(self):
        """Abstract method, return DAO maintenance physical classes, used to query statements
                 : return .class
        """
        pass

    def find_by_id(self, ids):
        """Id look up
                 : Param IDS integer type
                 : ReturN instance
        """
        return session.query(self.get_entityclass()).filter(self.get_entityclass().id == ids).one()



class EntryNotFoundException(Exception):
    pass


class ObjectNotMatchException(Exception):
    pass


if __name__ == '__main__':
    d = dao()
    d.create(Task())
