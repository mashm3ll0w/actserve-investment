from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from investments.models import InvestmentAccount, Transaction, UserAccount
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


class InvestmentAccountAPITestCase(APITestCase):
    def setUp(self):
        # create users
        first_user = self.client.post(path='/api/users/',
                                      data={'username': 'testuser', 'password': 'password',
                                            'email': 'test_user@mail.com', 'first_name': 'Test',
                                            'last_name': 'User'})
        admin_user = self.client.post(path='/api/users/',
                                      data={'username': 'admin', 'password': 'adminpassword',
                                            'email': 'admin_user@mail.com', 'first_name': 'Admin',
                                            'last_name': 'User'})

        self.first_user = User.objects.get(email=first_user.data['email'])
        self.admin_user = User.objects.get(email=admin_user.data['email'])
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.investment_account1 = InvestmentAccount.objects.create(name='Account 1', description='View Only Account', balance=1000)
        self.investment_account2 = InvestmentAccount.objects.create(name='Account 2', description='Full CRUD Account', balance=5000)
        self.user_account1 = UserAccount.objects.create(user=self.first_user, investment_account=self.investment_account1, permissions=UserAccount.VIEW_ONLY)
        self.user_account2 = UserAccount.objects.create(user=self.admin_user, investment_account=self.investment_account2, permissions=UserAccount.FULL_CRUD)

    def test_create_user(self):
        response = self.client.post(path='/api/users/',
                                      data={'username': 'dummyuser', 'password': 'password',
                                            'email': 'dummy@mail.com', 'first_name': 'Dummy',
                                            'last_name': 'Dummy'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'dummyuser')
        self.assertEqual(response.data['first_name'], 'Dummy')
        self.assertEqual(response.data['last_name'], 'Dummy')
        self.assertEqual(response.data['email'], 'dummy@mail.com')

    def test_cannot_view_without_permissions(self):
        response = self.client.get(f'/api/users/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.first_user)
        return str(refresh.access_token)

    def test_authenticated_access(self):
        access_token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(f'/api/users/{self.first_user.id}/')
        self.assertEqual(response.status_code, 200)

    def get_admin_token(self):
        refresh = RefreshToken.for_user(self.admin_user)
        return str(refresh.access_token)

    def test_access_admin_view_with_admin(self):
        access_token = self.get_admin_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(f'/api/user_transactions/{self.investment_account2.id}')
        self.assertEqual(response.status_code, 200)

    def test_access_admin_view_with_non_admin(self):
        access_token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(f'/api/user_transactions/{self.investment_account2.id}')
        self.assertEqual(response.status_code, 403)

