import random

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from faker_commerce import Provider as CommerceProvider
from tqdm import tqdm

from forum.models import Comment, Post
from gifts.models import Gift, GiftCategory, Review, ReviewVote
from hobbies.models import Hobby
from users.models import User


class Command(BaseCommand):
    help = "Seed the database with random data"

    def handle(self, *args, **options):
        fake = Faker()
        fake.add_provider(CommerceProvider)

        seeder = Seed.seeder()

        hobbies = list(Hobby.objects.all())
        categories = list(GiftCategory.objects.all())

        # Seed Users
        seeder.add_entity(
            User,
            200,
            {
                "bio": lambda x: seeder.faker.text(max_nb_chars=100),
                "location": lambda x: seeder.faker.city(),
            },
        )

        seeder.execute()

        users = list(User.objects.all())
        for user in users:
            user.hobbies.set(
                random.sample(hobbies, random.randint(1, min(len(hobbies), 5)))
            )
            friends = random.sample(
                [u for u in users if u != user],
                random.randint(0, min(len(users) - 1, 10)),
            )
            user.friends.set(friends)

        # Seed Gifts
        num_gifts = 200
        for _ in tqdm(range(num_gifts), desc="Created Gifts", unit="gift"):
            priceMin = random.uniform(1.0, 500.0)
            gift = Gift.objects.create(
                name=fake.ecommerce_name(),
                description=seeder.faker.text(max_nb_chars=200),
                priceMin=priceMin,
                priceMax=priceMin + random.uniform(5.0, 2000.0),
                suggestedBy=random.choice(users),
                suitable_age_range=random.choice(
                    [choice[0] for choice in Gift.AGE_RANGE_CHOICES]
                ),
                suitable_gender=random.choice(
                    [choice[0] for choice in Gift.GENDER_CHOICES]
                ),
            )
            gift.hobbies.set(random.sample(hobbies, random.randint(1, 5)))
            gift.giftCategories.set(random.sample(categories, random.randint(1, 5)))

            try:
                image_url = (
                    f"https://picsum.photos/300/300?random={random.randint(1, 10000)}"
                )
                response = requests.get(image_url, timeout=5)

                if response.status_code == 200:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()
                    gift.image.save(f"gift_{gift.pk}.jpg", File(img_temp), save=True)
            except requests.exceptions.RequestException:
                pass

        # Seed Posts and Comments
        seeder.add_entity(
            Post,
            15,
            {
                "author": lambda x: random.choice(users),
            },
        )
        seeder.add_entity(
            Comment,
            30,
            {
                "author": lambda x: random.choice(users),
                "post": lambda x: random.choice(Post.objects.all()),
            },
        )
        seeder.execute()

        # Seed Reviews...
        for user in users:
            num_reviews = random.randint(-3, 10)
            if num_reviews > 0:
                gifts = random.sample(list(Gift.objects.all()), num_reviews)
                for gift in gifts:
                    Review.objects.create(
                        gift=gift,
                        author=user,
                        title=seeder.faker.sentence(),
                        content=seeder.faker.text(),
                        rating=random.randint(1, 5),
                    )

        # ...and Votes
        for user in users:
            num_votes = random.randint(0, 20)
            reviews_to_vote = random.sample(
                list(Review.objects.exclude(author=user)), num_votes
            )
            for review in reviews_to_vote:
                ReviewVote.objects.create(
                    review=review,
                    user=user,
                    vote=random.choice([-1, 1]),  # 50% upvote, 50% downvote
                )

        self.stdout.write(self.style.SUCCESS("Database successfully seeded!"))
