# mock.py
import os
from dotenv import load_dotenv
from decimal import Decimal

# โหลดค่า .env
load_dotenv()

from app import create_app
from models.user import db, User
from models.book import Book
from models.book_categories import BookCategory
from models.order import Order, StatusEnum
from models.order_item import OrderItem

# สร้าง app จาก factory
app = create_app()

print("→ Using DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
print("→ DB_USER:", os.getenv("DB_USER"))
print("→ DB_NAME:", os.getenv("DB_NAME"))

with app.app_context():
    try:
        db.drop_all()
        db.create_all()

        # Categories
        categories = [
            BookCategory(name="Action"), # 0
            BookCategory(name="Adeventure"), # 1
            BookCategory(name="Fantasy"), # 2
            BookCategory(name="Isakai"), # 3
            BookCategory(name="Romance&Comedy"), # 4
            BookCategory(name="Sci-fi"), # 5
            BookCategory(name="Harem"), # 6
            BookCategory(name="Drama"), # 7
            BookCategory(name="School_life"), # 8
            BookCategory(name="Sport"), # 9
            BookCategory(name="Mystery"), # 10
            BookCategory(name="Horror"), # 11
            BookCategory(name="Psychological"), # 12
            BookCategory(name="Supernatural"), # 13
            BookCategory(name="Historical"), # 14
            BookCategory(name="Martial Art"), # 15
            BookCategory(name="Military"), # 16
            BookCategory(name="Music"), # 17
            BookCategory(name="Superhero"), # 18
            BookCategory(name="NTR"), # 19
            BookCategory(name="Game"), # 20

        ]

        # Users
        users = [
            User(name="Alice", email="alice@example.com", password_hash="1234", role="user"),
            User(name="Bob", email="bob@example.com", password_hash="1234", role="stock_keeper"),
            User(name="Admin", email="admin@example.com", password_hash="1234", role="admin"),
        ]

        # Books
        books = [
            Book(
                title="ยอดนักสืบจิ๋ว โคนัน เล่ม 1",
                author="โกโช อะโอะยะมะ",
                price=Decimal("69.00"),
                stock_quantity=18,
                image_path="assets/minidetecive01.jpg",
                category=categories[0],
            ),
            Book(
                title="ยอดนักสืบจิ๋ว โคนัน เล่ม 2",
                author="โกโช อะโอะยะมะ",
                price=Decimal("69.00"),
                stock_quantity=13,
                image_path="assets/minidetecive02.jpg",
                category=categories[0],
            ),
            Book(
                title="ยอดนักสืบจิ๋ว โคนัน เล่ม 3",
                author="โกโช อะโอะยะมะ",
                price=Decimal("69.00"),
                stock_quantity=16,
                image_path="assets/minidetecive03.jpg",
                category=categories[0],
            ),
            Book(
                title="ยอดนักสืบจิ๋ว โคนัน เล่ม 4",
                author="โกโช อะโอะยะมะ",
                price=Decimal("69.00"),
                stock_quantity=20,
                image_path="assets/minidetecive04.jpg",
                category=categories[0],
            ),
            Book(
                title="CHAIN SAW MAN เล่ม 1",
                author="ฟูจิโมโตะ ทัตสึกิ",
                price=Decimal("99.00"),
                stock_quantity=11,
                image_path="assets/CHAINSAWMAN01.jpg",
                category=categories[0],
            ),
            Book(
                title="CHAIN SAW MAN เล่ม 2",
                author="ฟูจิโมโตะ ทัตสึกิ",
                price=Decimal("99.00"),
                stock_quantity=11,
                image_path="assets/CHAINSAWMAN02.jpg",
                category=categories[0],
            ),
            Book(
                title="มหาเวทย์ผนึกมาร เล่ม 1",
                author="เกเงะ อากูตามิ",
                price=Decimal("99.00"),
                stock_quantity=1,
                image_path="assets/JujutsuKaisen01.jpg",
                category=categories[1],
            ),
            Book(
                title="มหาเวทย์ผนึกมาร เล่ม 2",
                author="เกเงะ อากูตามิ",
                price=Decimal("99.00"),
                stock_quantity=2,
                image_path="assets/JujutsuKaisen02.jpg",
                category=categories[1],
            ),
            Book(
                title="มหาเวทย์ผนึกมาร เล่ม 3",
                author="เกเงะ อากูตามิ",
                price=Decimal("99.00"),
                stock_quantity=0,
                image_path="assets/JujutsuKaisen03.jpg",
                category=categories[1],
            ),
            Book(
                title="86 เอทตี้ซิกซ์ เล่ม 1",
                author="อาซาโตะ อาซาโตะ, ชิราบิ",
                price=Decimal("300.00"),
                stock_quantity=4,
                image_path="assets/86_01.jpg",
                category=categories[5],
            ),
            Book(
                title="นักสืบตายแล้ว เล่ม 1",
                author="นิโกะ จูยุ",
                price=Decimal("255.00"),
                stock_quantity=15,
                image_path="assets/book1.jpg",
                category=categories[10],
            ),
            Book(
                title="แมงมุมแล้วไง ข้องใจเหรอคะ เล่ม 1",
                author="โอกินะ บาบะ",
                price=Decimal("230.00"),
                stock_quantity=5,
                image_path="assets/spiderwoman01.jpg",
                category=categories[2],
            ),
            Book(
                title="จันทรานำพาสู่ต่างโลก เล่ม 1",
                author="อาสึกิ",
                price=Decimal("293.00"),
                stock_quantity=3,
                image_path="assets/tothemoon01.jpg",
                category=categories[3],
            ),
            Book(
                title="Solo Leveling เล่ม 1",
                author="ชูกง",
                price=Decimal("255.00"),
                stock_quantity=8,
                image_path="assets/solosigma01.jpg",
                category=categories[0],
            ),
            Book(
                title="มุมมองนักอ่านพระเจ้า เล่ม 1",
                author="ซิงชอง",
                price=Decimal("266.00"),
                stock_quantity=5,
                image_path="assets/godreader01.jpg",
                category=categories[0],
            ),
            Book(
                title="สุดยอดมือสังหารอวตารมาต่างโลก เล่ม 1",
                author="รุย สึกิโยะ",
                price=Decimal("295.00"),
                stock_quantity=5,  # กำหนดเองได้
                image_path="assets/padoharem01.jpg",
                category=categories[6],
            ),
            Book(
                title="ชมรมรัก คลับมหาสนุก เล่ม 1",
                author="Bisco Hatori",
                price=Decimal("49.00"),
                stock_quantity=7,
                image_path="assets/Loveclub01.jpg",
                category=categories[4],
            ),
            Book(
                title="ชมรมรัก คลับมหาสนุก เล่ม 2",
                author="Bisco Hatori",
                price=Decimal("49.00"),
                stock_quantity=14,
                image_path="assets/Loveclub02.jpg",
                category=categories[4],
            ),
            Book(
                title="ชมรมรัก คลับมหาสนุก เล่ม 3",
                author="Bisco Hatori",
                price=Decimal("49.00"),
                stock_quantity=9,
                image_path="assets/Loveclub03.jpg",
                category=categories[4],
            ),
            Book(
                title="ชมรมรัก คลับมหาสนุก เล่ม 4",
                author="Bisco Hatori",
                price=Decimal("49.00"),
                stock_quantity=20,
                image_path="assets/Loveclub04.jpg",
                category=categories[4],
            ),
            Book(
                title="ชมรมรัก คลับมหาสนุก เล่ม 5",
                author="Bisco Hatori",
                price=Decimal("49.00"),
                stock_quantity=6,
                image_path="assets/Loveclub05.jpg",
                category=categories[4],
            ),
            Book(
                title="จอมมารเกิดใหม่ วิทยาลัยผู้พิทักษ์ เล่ม 1",
                author="ยู ชิมิซุ",
                price=Decimal("169.00"),
                stock_quantity=11,
                image_path="assets/minidemonloard01.jpg",
                category=categories[6],
            ),
            Book(
                title="จอมมารเกิดใหม่ วิทยาลัยผู้พิทักษ์ เล่ม 2",
                author="ยู ชิมิซุ",
                price=Decimal("169.00"),
                stock_quantity=4,
                image_path="assets/minidemonloard02.jpg",
                category=categories[6],
            ),
            Book(
                title="หนุ่มซิงกับสาวฮอต เดตนี้จะรอดมั้ยนะ เล่ม 1",
                author="มากิโกะ นางาโอกะ",
                price=Decimal("149.00"),
                stock_quantity=7,
                image_path="assets/verginmanandhotgirl01.jpg",
                category=categories[7],
            ),
            Book(
                title="หนุ่มซิงกับสาวฮอต เดตนี้จะรอดมั้ยนะ เล่ม 2",
                author="มากิโกะ นางาโอกะ",
                price=Decimal("149.00"),
                stock_quantity=13,
                image_path="assets/verginmanandhotgirl02.jpg",
                category=categories[7],
            ),
            Book(
                title="แผน NTR แฟนรุ่นพี่แค้นนี้ต้องชำระ เล่ม 1",
                author="มิฮิโระ ชินเด็น",
                price=Decimal("295.00"),
                stock_quantity=5,
                image_path="assets/revengntr01.jpg",
                category=categories[19],
            ),
            Book(
                title="แผน NTR แฟนรุ่นพี่แค้นนี้ต้องชำระ เล่ม 2",
                author="มิฮิโระ ชินเด็น",
                price=Decimal("295.00"),
                stock_quantity=2,
                image_path="assets/revengntr02.jpg",
                category=categories[19],
            ),
            Book(
                title="เพื่อนคนแรกของผมคือสาวสวยอันดับสองของห้อง เล่ม 1",
                author="ทาคาตะ",
                price=Decimal("305.00"),
                stock_quantity=4,
                image_path="assets/myfriendistheseconbeautifulgiryinschool01.jpg",
                category=categories[8],
            ),
            Book(
                title="เพื่อนคนแรกของผมคือสาวสวยอันดับสองของห้อง เล่ม 2",
                author="ทาคาตะ",
                price=Decimal("305.00"),
                stock_quantity=6,
                image_path="assets/myfriendistheseconbeautifulgiryinschool02.jpg",
                category=categories[8],
            ),
            Book(
                title="Deep3 เล่ม 1",
                author="TOBIMATSU RYOUSUKE",
                price=Decimal("99.00"),
                stock_quantity=9,
                image_path="assets/Deep3_01.jpg",
                category=categories[9],
            ),
            Book(
                title="Deep3 เล่ม 2",
                author="TOBIMATSU RYOUSUKE",
                price=Decimal("99.00"),
                stock_quantity=7,
                image_path="assets/Deep3_02.jpg",
                category=categories[9],
            ),
            Book(
                title="Deep3 เล่ม 3",
                author="TOBIMATSU RYOUSUKE",
                price=Decimal("99.00"),
                stock_quantity=5,
                image_path="assets/Deep3_03.jpg",
                category=categories[9],
            ),
            Book(
                title="Your friend คำสาปเพื่อนตาย",
                author="ซาวามูระ อิจิ",
                price=Decimal("299.00"),
                stock_quantity=11,
                image_path="assets/Yourfrienddie.jpg",
                category=categories[11],
            ),
            Book(
                title="ให้ฉันช่วยฆ่าให้เอาไหม",
                author="โคบายาชิ ยุกะ",
                price=Decimal("276.00"),
                stock_quantity=8,
                image_path="assets/letmekillthemforyou.jpg",
                category=categories[11],
            ),
            Book(
                title="9 สิงหา ผวารักวิปริต เล่ม 1",
                author="tomomi",
                price=Decimal("145.00"),
                stock_quantity=7,
                image_path="assets/9agus01.jpg",
                category=categories[12],
            ),
            Book(
                title="9 สิงหา ผวารักวิปริต เล่ม 2",
                author="tomomi",
                price=Decimal("145.00"),
                stock_quantity=4,
                image_path="assets/9agus02.jpg",
                category=categories[12],
            ),
            Book(
                title="คดีประหลาด คนปีศาจ เล่ม 1",
                author="Sho Aimoto",
                price=Decimal("95.00"),
                stock_quantity=6,
                image_path="assets/humandemon01.jpg",
                category=categories[13],
            ),
            Book(
                title="คดีประหลาด คนปีศาจ เล่ม 2",
                author="Sho Aimoto",
                price=Decimal("95.00"),
                stock_quantity=14,
                image_path="assets/humandemon02.jpg",
                category=categories[13],
            ),
            Book(
                title="คดีประหลาด คนปีศาจ เล่ม 3",
                author="Sho Aimoto",
                price=Decimal("95.00"),
                stock_quantity=9,
                image_path="assets/humandemon03.jpg",
                category=categories[13],
            ),
            Book(
                title="ประวัติศาสตร์รัสเซีย",
                author="ภาณุดา วงศ์พรหม",
                price=Decimal("399.00"),
                stock_quantity=20,
                image_path="assets/russiahistory.jpg",
                category=categories[14],
            ),
            Book(
                title="ประวัติศาสตร์ญี่ปุ่น",
                author="อาร์.เอช.พี.เมสัน, เจ.จี.เคเกอร์",
                price=Decimal("399.00"),
                stock_quantity=15,
                image_path="assets/japanhistory.jpg",
                category=categories[14],
            ),
            Book(
                title="ประวัติศาสตร์อเมริกา",
                author="เริงวุฒิ มิตรสุริยะ",
                price=Decimal("522.50"),
                stock_quantity=18,
                image_path="assets/usahistory.jpg",
                category=categories[14],
            ),
            Book(
                title="ข้าไม่ได้อยากเป็นประมุขมารเลยสักนิด",
                author="เกาทัณฑ์ไฟ",
                price=Decimal("170.05"),
                stock_quantity=12,
                image_path="assets/HowtobeanEvilMartialArts.jpg",
                category=categories[15],
            ),
            Book(
                title="สงครามโลกครั้งที่1,2 ฉ.สมบูรณ์",
                author="วีระชัย โชคมุกดา",
                price=Decimal("575.00"),
                stock_quantity=14,
                image_path="assets/HowtobeanEvilMartialArts2.jpg",
                category=categories[16],
            ),
            Book(
                title="CHIP WAR สงครามชิป",
                author="Chris Miller",
                price=Decimal("351.00"),
                stock_quantity=7,
                image_path="assets/chipwar.jpg",
                category=categories[16],
            ),
            Book(
                title="MUSIC 1ST EDITION BORN TO BE ALBUM BY PIPT",
                author="พรทิพย์ ภัทรวิทย์",
                price=Decimal("293.00"),
                stock_quantity=10,
                image_path="assets/musicborntobe.jpg",
                category=categories[17],
            ),
            Book(
                title="MY SUPERHERO EX'S",
                author="อนาเซีย",
                price=Decimal("249.00"),
                stock_quantity=5,
                image_path="assets/mysuperheroex.jpg",
                category=categories[18],
            ),
            Book(
                title="โนเกม โนไลฟ์ เล่ม 1 (no game no life)",
                author="ยู คามิยะ",
                price=Decimal("200.00"),
                stock_quantity=8,
                image_path="assets/nogamenolife01.jpg",
                category=categories[20],
            ),
            Book(
                title="โนเกม โนไลฟ์ เล่ม 2 (no game no life)",
                author="ยู คามิยะ",
                price=Decimal("200.00"),
                stock_quantity=6,
                image_path="assets/nogamenolife02.jpg",
                category=categories[20],
            ),
            Book(
                title="โนเกม โนไลฟ์ เล่ม 3 (no game no life)",
                author="ยู คามิยะ",
                price=Decimal("200.00"),
                stock_quantity=4,
                image_path="assets/nogamenolife03.jpg",
                category=categories[20],
            ),
        ]

        db.session.add_all(categories + users + books)
        db.session.commit()

        # Orders
        order1 = Order(
            user=users[0],
            status=StatusEnum.pending,
            total_amount=Decimal("749.00"),
        )

        # Order Items
        from datetime import datetime, timedelta
        now = datetime.now()
        order1_item1 = OrderItem(
            order=order1,
            book_title=books[0].title,
            book_author=books[0].author,
            book_image_path=books[0].image_path,
            quantity=1,
            unit_price=Decimal("299.00"),
            created_at=now - timedelta(days=1)
        )
        order1_item2 = OrderItem(
            order=order1,
            book_title=books[1].title,
            book_author=books[1].author,
            book_image_path=books[1].image_path,
            quantity=1,
            unit_price=Decimal("450.00"),
            created_at=now
        )

        db.session.add_all([order1, order1_item1, order1_item2])
        db.session.commit()

        print("✅ Mock data inserted successfully!")

    except Exception as e:
        print("❌ Error while seeding mock data:", e)
