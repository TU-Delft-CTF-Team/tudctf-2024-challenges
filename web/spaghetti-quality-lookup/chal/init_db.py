import sqlite3
import os

con = sqlite3.connect("spaghetti.db")
cur = con.cursor()

cur.execute("CREATE TABLE flags(flag)")
cur.execute(f"INSERT INTO flags VALUES ('{os.environ['FLAG']}')")

cur.execute("CREATE TABLE spaghetti_types(id, spaghetti, qualities)")
cur.execute("""
            INSERT INTO spaghetti_types VALUES
            (1, 'Spaghetti', 'Classic long, thin pasta; versatile for most sauces (tomato, cream, oil-based, etc.). Best served with pineapple and ketchup.'),
            (2, 'Spaghettini', 'Thinner than standard spaghetti; cooks quickly; best with lighter sauces or seafood.'),
            (3, 'Spaghetti alla Chitarra', 'Square-shaped strands; slightly thicker; holds onto hearty sauces like meat or thick tomato.'),
            (4, 'Bucatini', 'Thick spaghetti with a hollow center; chewy texture; ideal for rich, thick sauces like amatriciana.'),
            (5, 'Capellini (Angel Hair)', 'Extremely thin and delicate; pairs best with light, oil-based or broth sauces.'),
            (6, 'Vermicelli', 'Slightly thicker than capellini but still fine; best with light or simple sauces.'),
            (7, 'Pici', 'Thick, hand-rolled pasta from Tuscany; chewy and rustic; pairs well with thick, hearty sauces.'),
            (8, 'Fedelini', 'Slightly thicker than angel hair; good with delicate, mild sauces or light seafood dishes.'),
            (9, 'Linguine', 'Flat, ribbon-like; good with cream sauces, pesto, and seafood.'),
            (10, 'Fettuccine', 'Flat, wider than linguine; excellent for rich, creamy sauces like Alfredo or bolognese.'),
            (11, 'Tagliatelle', 'Similar to fettuccine but slightly narrower; works with ragù, mushroom, or truffle sauces.'),
            (12, 'Bigoli', 'Thick, long, and rough; best with hearty sauces, particularly meat-based or game sauces.'),
            (13, 'Spaghetti Rigati', 'Spaghetti with ridges; helps the pasta hold onto chunkier sauces.'),
            (14, 'Tonnarelli', 'Similar to spaghetti alla chitarra, but thicker; ideal for carbonara or cacio e pepe.'),
            (15, 'Spaghetti al Nero di Seppia', 'Infused with squid ink; dark color and briny flavor; pairs well with seafood.'),
            (16, 'Gluten-Free Spaghetti', 'Made from rice, quinoa, or corn; caters to gluten-intolerant; can have different textures.'),
            (17, 'Whole Wheat Spaghetti', 'Nutty flavor, higher fiber content; slightly denser texture, best with robust sauces.'),
            (18, 'Zucchini Spaghetti (Zoodles)', 'Spiralized zucchini as a low-carb option; fresh, light; pairs well with pesto or tomato sauces.'),
            (19, 'Spaghetti Integrali', 'Whole grain spaghetti with earthy flavor; nutritious and pairs well with bold sauces.'),
            (20, 'Chickpea Spaghetti', 'Made from chickpeas; high protein and fiber; nutty flavor, best with Mediterranean-style sauces.'),
            (21, 'Brown Rice Spaghetti', 'Gluten-free; mild flavor; slightly chewier texture, good for simple vegetable or seafood sauces.'),
            (22, 'Spinach Spaghetti', 'Infused with spinach for a green hue and mild vegetal flavor; best with light sauces.'),
            (23, 'Protein-Enriched Spaghetti', 'Made with additional protein (often from legumes); firmer texture, best with hearty sauces.'),
            (24, 'Corn Spaghetti', 'Gluten-free; slightly sweet taste; best with rich, creamy sauces to balance the flavor.'),
            (25, 'Squid Ink Spaghetti', 'Infused with squid ink, giving a briny flavor; pairs well with seafood-based sauces.');
            """)
con.commit()
