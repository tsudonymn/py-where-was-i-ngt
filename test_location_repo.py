import unittest
from location_repo import LocationRepo

class TestLocationRepo(unittest.TestCase):
    def test_load_locations(self):
        test_data = [
            {
                "placeId": "ChIJAAAAAAAAAAARYOAlcSt2CHw",
                "placeLocation": "42.2504552°, -83.7649476°",
                "label": "1545"
            },
            {
                "placeId": "ChIJAAAAAAAAAAAR4AosrBcexFk",
                "placeLocation": "42.2919604°, -83.7333239°",
                "label": "1410"
            }
        ]
        
        repo = LocationRepo(json.dumps(test_data))
        
        # Verify locations are loaded correctly
        self.assertEqual(len(repo.locations), 2)
        self.assertEqual(repo.locations[0].placeId, "ChIJAAAAAAAAAAARYOAlcSt2CHw")
        self.assertEqual(repo.locations[0].placeLocation, "42.2504552°, -83.7649476°")
        self.assertEqual(repo.locations[0].label, "1545")
        
        self.assertEqual(repo.locations[1].placeId, "ChIJAAAAAAAAAAAR4AosrBcexFk")
        self.assertEqual(repo.locations[1].placeLocation, "42.2919604°, -83.7333239°")
        self.assertEqual(repo.locations[1].label, "1410")
        
        # Verify placeId_dict
        self.assertEqual(len(repo.placeId_dict), 2)
        self.assertIn("ChIJAAAAAAAAAAARYOAlcSt2CHw", repo.placeId_dict)
        self.assertIn("ChIJAAAAAAAAAAAR4AosrBcexFk", repo.placeId_dict)

if __name__ == "__main__":
    unittest.main()