from plainvoice.model.base import Base


class ClientsList(Base):
    """
    This class controlls the list for clients.
    """

    def get_all_client_ids(self) -> list[str]:
        """
        Get all the client ids from the clients folder.

        Returns:
            list: The list containing client id strings.
        """
        out = []
        return out

    def id_exists(self, client_id: str) -> bool:
        """
        Checks if the client id exists in the clients
        folder already.

        Args:
            client_id (str): The client id.

        Returns:
            bool: Returns True if client id already exists.
        """
        return client_id in self.get_all_client_ids()
