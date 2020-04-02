from inferno.db.Models import Recommendation


class MongoRepository:

    def fetch_all_documents(self):
        try:
            recommendations = Recommendation.objects.to_json()
            return {
                'status': True,
                'result': 'All documents fetched successfully',
                'data': recommendations,
                'error': None
            }
        except Exception as ex:
            return {
                'status': False,
                'result': None,
                'data': None,
                'error': ex
            }

    def text_search(self, term):
        try:
            objects = Recommendation.objects.search_text(term)
            if objects:
                return {
                    'status': True,
                    'result': 'Text search successful',
                    'data': objects,
                    'error': None
                }
        except Exception as ex:
            return {
                'status': False,
                'result': None,
                'data': None,
                'error': ex
            }

    def truncate_collection(self):
        try:
            Recommendation.objects.delete()
            return {
                'status': True,
                'result': 'Collection truncated successfully',
                'data': None,
                'error': None
            }
        except Exception as ex:
            return {
                'status': False,
                'result': None,
                'data': None,
                'error': ex
            }

    def batch_insert(self, spread_documents):
        try:
            batch_insert_status = Recommendation.objects.insert(spread_documents)
            if batch_insert_status:
                return {
                    'status': True,
                    'result': 'Batch inserted successfully',
                    'data': batch_insert_status,
                    'error': None
                }
        except Exception as ex:
            return {
                'status': False,
                'result': None,
                'data': None,
                'error': ex
            }
