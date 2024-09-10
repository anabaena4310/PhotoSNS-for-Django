from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
from .models import Post, Tag
from pathlib import Path
import time


BASE_DIR = Path(__file__).resolve().parent.parent


class UserRegistrationTest(TestCase):
    def test_user_registration_success(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクトを確認
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())


    def test_user_registration_password_mismatch(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'WrongPass123!'
        })
        form = response.context['form']  
        self.assertEqual(response.status_code, 200)  # フォーム再表示
        self.assertFormError(form, 'password2', "You must type the same password each time.")
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())


class LoginTests(TestCase):
    def setUp(self):
        # テスト用のユーザーを作成
        self.username = 'testuser'
        self.password = 'password123'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

    def test_login_success(self):
        # ログインページのURLを逆引き
        login_url = reverse('account_login')  # allauthのlogin URLパターン名を使用
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)

        # 正しいクレデンシャルでログインを試みる
        response = self.client.post(login_url, {
            'login': self.username,  # allauthでは 'login' がユーザー名/メールアドレスのフィールド名
            'password': self.password
        })

        # リダイレクト先が存在するか確認（ログイン後のリダイレクト）
        self.assertRedirects(response, reverse('home'))  # ログイン後のリダイレクト先URLに変更する
        self.assertEqual(response.status_code, 302)

    def test_login_failure(self):
        # ログインページのURLを逆引き
        login_url = reverse('account_login')
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)

        # 不正なクレデンシャルでログインを試みる
        response = self.client.post(login_url, {
            'login': self.username,
            'password': 'wrongpassword'
        })

        # ログインが失敗した場合、同じページに戻ることを確認
        self.assertEqual(response.status_code, 200)
        # ログイン失敗後、home画面にアクセスできないことを確認
        home_url = reverse('home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 302)  # ログインページにリダイレクト
        self.assertFalse(response.url == home_url)



class PostCreationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='poster', password='ComplexPass123!')
        Tag.objects.create(name='test-tag')

    def test_create_post_success(self):
        self.client.login(username='poster', password='ComplexPass123!')
        image_path = BASE_DIR / 'media' / 'images' / 'N811_konekocyan.jpg'  # {{ edit_1 }} - パスの結合方法を修正
        with open(image_path, 'rb') as img:  # {{ edit_2 }} - 修正されたパスを使用
            response = self.client.post(reverse('create_post'), {
                'image': img,
                'caption': 'Test Caption',
                'tags': Tag.objects.filter(name='test-tag').values_list('id', flat=True)  
            })
        self.assertEqual(response.status_code, 302)  # リダイレクトを確認
        self.assertTrue(Post.objects.filter(caption='Test Caption').exists())


    def test_create_post_no_image(self):
        self.client.login(username='poster', password='ComplexPass123!')
        response = self.client.post(reverse('create_post'), {
            'caption': 'Test Caption',
            'tags': Tag.objects.filter(name='test-tag').values_list('id', flat=True)  
        })
        form = response.context['form']  
        self.assertEqual(response.status_code, 200)  # フォーム再表示
        self.assertFormError(form, 'image', 'This field is required.')
        self.assertFalse(Post.objects.filter(caption='Test Caption').exists())


class FollowUnfollowTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='Pass123!')
        self.user2 = CustomUser.objects.create_user(username='user2', password='Pass123!')
        self.client.login(username='user2', password='Pass123!')
        with open(BASE_DIR / 'media' / 'images' / 'N811_konekocyan.jpg', 'rb') as img:  # {{ edit_2 }} - 修正されたパスを使用
            self.user2_post = self.client.post(reverse('create_post'), {
                'image': img,
                'caption': 'This is a test post from user2',
                'tags': Tag.objects.filter(name='test-tag').values_list('id', flat=True)  
            })

    def test_follow_user(self):
        self.client.login(username='user1', password='Pass123!')
        most_recent_post_id = Post.objects.latest('id').id
        response = self.client.post(reverse('follow_unfollow_user', args=[most_recent_post_id])) 
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user1.following.filter(id=self.user2.id).exists())

    def test_unfollow_user(self):
        # 事前にフォローしておく
        self.user1.following.set([self.user2.id])  # {{ edit_1 }} - set()メソッドを使用してフォローを設定
        self.assertTrue(self.user1.following.filter(id=self.user2.id).exists())
        self.client.login(username='user1', password='Pass123!')
        most_recent_post_id = Post.objects.latest('id').id
        response = self.client.post(reverse('follow_unfollow_user', args=[most_recent_post_id])) 
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user1.following.filter(id=self.user2.id).exists())


class TimelineTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='Pass123!')
        self.user2 = CustomUser.objects.create_user(username='user2', password='Pass123!')
        self.client.login(username='user2', password='Pass123!')
        with open(BASE_DIR / 'media' / 'images' / 'N811_konekocyan.jpg', 'rb') as img:  # {{ edit_2 }} - 修正されたパスを使用
            self.user2_post = self.client.post(reverse('create_post'), {
                'image': img,
                'caption': 'This is a test post from user2',
                'tags': Tag.objects.filter(name='test-tag').values_list('id', flat=True)  
            })
        self.client.login(username='user1', password='Pass123!')
        self.user1.following.set([self.user2.id])

    def test_following_timeline(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('This is a test post from user2' in response.content.decode())

    def test_following_timeline_delete_user(self):
        self.user2.delete()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('This is a test post from user2' in response.content.decode())


class XSSProtectionTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user', password='Pass123!')

    def test_xss_injection_in_caption(self):
        self.client.login(username='user', password='Pass123!')
        xss_payload = '<script>alert("XSS")</script>'
        with open(BASE_DIR / 'media' / 'images' / 'N811_konekocyan.jpg', 'rb') as img:  # {{ edit_2 }} - 修正されたパスを使用
            self.user2_post = self.client.post(reverse('create_post'), {
                'image': img,
                'caption': xss_payload,
                'tags': Tag.objects.filter(name='test-tag').values_list('id', flat=True)  
            })
        post = Post.objects.get(caption=xss_payload)
        response = self.client.get(reverse('post_detail', args=[post.id]))
        print(response)
        self.assertNotContains(response, xss_payload)
        self.assertContains(response, "&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;")


class SQLInjectionTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user', password='Pass123!')

    def test_sql_injection_on_login(self):
        response = self.client.post(reverse('account_login'), {
            'username': "user' OR '1'='1",
            'password': 'irrelevant'
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "If you have not created an account yet, then please ")


class PerformanceTest(TestCase):
    def test_timeline_response_time(self):
        self.user = CustomUser.objects.create_user(username='user', password='Pass123!')
        self.viewer_user = CustomUser.objects.create_user(username='viewer', password='ViewerPass123!')
        self.client.login(username='user', password='Pass123!')        
        # タイムラインに多数の投稿を作成
        for i in range(100):
            with open(BASE_DIR / 'media' / 'images' / 'N811_konekocyan.jpg', 'rb') as img:
                self.client.post(reverse('create_post'), {
                    'image': img,
                    'caption': f'Post {i}',
                    'tags': Tag.objects.filter(name='test-tag').values_list('id', flat=True)  
                })
        self.client.login(username='viewer', password='ViewerPass123!')
        self.client.post(reverse('follow_unfollow_user', args=[Post.objects.latest('id').id]))
        start_time = time.time()
        response = self.client.get(reverse('home'))
        end_time = time.time()
        response_time = end_time - start_time
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1)  # レスポンスタイムが1秒未満であること