import server
from server import app


class TestShowSummary:
    """Tests the function showSummary()."""

    client_test = app.test_client()
    clubs_test = [
        {"name": "club TEST 01", "email": "club01@test.com", "points": "20"},
    ]

    def setup(self):
        """Change server.py variable datas."""
        server.clubs = self.clubs_test

    def test_good_email(self):
        """
        Test if the email is recognised: it returns (200).
        """
        result = self.client_test.post(
            "/showSummary", data={"email": self.clubs_test[0]["email"]}
        )
        assert result.status_code in [200]

    def test_bad_email(self):
        """
        Test if the email entered is not recognised : it redirects to the index (403).
        """
        result = self.client_test.post("/showSummary", data={"email": "test@test.com"})
        assert result.status_code in [403]


class TestBook:
    """
    Tests the function book().
    Clubs shouldn't be able to book places to old competitions.
    """

    client_test = app.test_client()
    clubs_test = [
        {"name": "club TEST 01", "email": "club01@test.com", "points": "20"},
    ]
    competitions_test = [
        {
            "name": "competition TEST 01",
            "date": "2030-05-12 10:00:00",
            "numberOfPlaces": "15",
        },
        {
            "name": "competition TEST 02",
            "date": "2010-05-12 10:00:00",
            "numberOfPlaces": "5",
        },
    ]

    def setup(self):
        """Change server.py variable datas."""
        server.clubs = self.clubs_test
        server.competitions = self.competitions_test

    def test_book_new_competition(self):
        """Test if the competition date >= today : it returns (200)."""
        result = self.client_test.get(
            "/book/"
            + self.competitions_test[0]["name"]
            + "/"
            + self.clubs_test[0]["name"]
        )
        assert result.status_code in [200]

    def test_book_old_competition(self):
        """Test if the competition date < today : it returns (403)."""
        result = self.client_test.get(
            "/book/"
            + self.competitions_test[1]["name"]
            + "/"
            + self.clubs_test[0]["name"]
        )
        assert result.status_code in [403]


class TestPurchasePlace:
    """
    Tests the function purchasePlace().
    Clubs shouldn't be able to use more than their points or available places."""

    client_test = app.test_client()
    clubs_test = [
        {"name": "club TEST 01", "email": "club01@test.com", "points": "20"},
        {"name": "club TEST 02", "email": "club02@test.com", "points": "3"},
    ]
    competitions_test = [
        {
            "name": "competition TEST 01",
            "date": "2030-05-12 10:00:00",
            "numberOfPlaces": "15",
        },
        {
            "name": "competition TEST 02",
            "date": "2020-05-12 10:00:00",
            "numberOfPlaces": "5",
        },
    ]

    def setup(self):
        """Change server.py variable datas."""
        server.clubs = self.clubs_test
        server.competitions = self.competitions_test

    def test_enough_points(self):
        """
        Test if club use enough points to buy places.
        If  points =< allowed points : it returns (200).
        """
        result = self.client_test.post(
            "/purchasePlaces",
            data={
                "places": 5,
                "club": self.clubs_test[0]["name"],
                "competition": self.competitions_test[0]["name"],
            },
        )
        assert result.status_code in [200]

    def test_not_enough_points(self):
        """
        Test if club use enough points to buy places.
        If club wants to use points > allowed points : it returns (403).
        """
        result = self.client_test.post(
            "/purchasePlaces",
            data={
                "places": 5,
                "club": self.clubs_test[1]["name"],
                "competition": self.competitions_test[0]["name"],
            },
        )
        assert result.status_code in [403]
        assert "More places requested than available points !" in result.data.decode()

    def test_not_positive_points(self):
        """
        Test if club wants to use point =< 0.
        """
        result = self.client_test.post(
            "/purchasePlaces",
            data={
                "places": -1,
                "club": self.clubs_test[0]["name"],
                "competition": self.competitions_test[0]["name"],
            },
        )
        assert result.status_code in [403]
        assert "This is not a positive value !!" in result.data.decode()

    def test_enough_places(self):
        """
        Test if club use more points than available places.
        If used points > availables places : it returns (403).
        """
        result = self.client_test.post(
            "/purchasePlaces",
            data={
                "places": 6,
                "club": self.clubs_test[0]["name"],
                "competition": self.competitions_test[1]["name"],
            },
        )
        assert result.status_code in [403]
        assert "More places requested than available !" in result.data.decode()

    def test_book_more_twelve_places(self):
        """
        Test to book 12 places per competition maximum.
        If used points > 12  : it returns (403).
        """
        result = self.client_test.post(
            "/purchasePlaces",
            data={
                "places": 13,
                "club": self.clubs_test[0]["name"],
                "competition": self.competitions_test[0]["name"],
            },
        )
        assert result.status_code in [403]
        assert "More places than authorized to book by club !" in result.data.decode()


class TestLog:

    client_test = app.test_client()

    def test_index(self):
        """Test acces to index page."""
        result = self.client_test.get("/")
        assert result.status_code in [200]

    def test_logout(self):
        """Test if the user logs out : it returns (302)."""
        response = self.client_test.get("/logout")
        assert response.status_code in [302]
