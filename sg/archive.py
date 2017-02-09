class Archive(object):
    def __init__(self, ar):
        self.__ar = ar

    def delete(self, vault_name, archive_id):
        l1 = self.__ar.get_l1()
        l1.delete_archive(vault_name, archive_id)
