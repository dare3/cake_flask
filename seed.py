from app import app, db
from models import Cupcake

def seed_cupcakes():
    cupcakes = [
        {'flavor': 'Chocolate', 'size': 'Medium', 'rating': 4.5},
        {'flavor': 'Vanilla', 'size': 'Small', 'rating': 4.0},
        {'flavor': 'Red Velvet', 'size': 'Large', 'rating': 5.0},
        {'flavor': 'Lemon', 'size': 'Medium', 'rating': 3.5},
    ]

    with app.app_context():
        for cupcake in cupcakes:
            new_cupcake = Cupcake(**cupcake)
            db.session.add(new_cupcake)
        db.session.commit()
        print("Cupcakes seeded successfully.")

if __name__ == '__main__':
    seed_cupcakes()
