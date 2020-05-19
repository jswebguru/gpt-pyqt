import os.path

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


class GPTLLamaIndexWrapper:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._directory = ''
        self._query_engine = None
        self._index = None

    def set_directory(self, directory):
        try:
            self._directory = directory
            documents = SimpleDirectoryReader(input_dir=self._directory, required_exts=['.txt']).load_data()
            self._index = VectorStoreIndex.from_documents(documents)
        except Exception as e:
            print(e)

    def is_query_engine_set(self):
        return self._query_engine

    def set_query_engine(self, streaming=False, similarity_top_k=3):
        if self._index is None:
            raise Exception('Index must be initialized first. Call set_directory or set_files first.')
        try:
            self._query_engine = self._index.as_query_engine(streaming=streaming,
                                                             similarity_top_k=similarity_top_k)
        except Exception as e:
            raise Exception(f'Error in setting query engine: {e}')

    def get_directory(self):
        """
        This function returns the directory path.
        If directory does not exist, it will return the empty string.
        """
        return self._directory if self._directory and os.path.exists(self._directory) else ''

    def get_response(self, text):
        try:
            if self._query_engine:
                resp = self._query_engine.query(
                    text,
                )
                return resp
            else:
                raise Exception('Query engine not initialized. Maybe you need to set the directory first. Check the directory path.')
        except Exception as e:
            return str(e)