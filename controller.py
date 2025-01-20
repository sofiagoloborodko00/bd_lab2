from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.add_category()
            elif choice == '2':
                self.update_category()
            elif choice == '3':
                self.delete_category()
            elif choice == '4':
                self.view_categories()
            elif choice == '5':
                self.add_seller()
            elif choice == '6':
                self.update_seller()
            elif choice == '7':
                self.delete_seller()
            elif choice == '8':
                self.view_sellers()
            elif choice == '9':
                self.add_product()
            elif choice == '10':
                self.update_product()
            elif choice == '11':
                self.delete_product()
            elif choice == '12':
                self.view_products()
            elif choice == '13':
                self.generate_data()
            elif choice == '14':
                self.query_top_categories()
            elif choice == '15':
                self.query_seller_products()
            elif choice == '16':
                self.query_category_seller_summary()
            elif choice == '17':
                break

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. Add Category")
        self.view.show_message("2. Update Category")
        self.view.show_message("3. Delete Category")
        self.view.show_message("4. View Categories")
        self.view.show_message("5. Add Seller")
        self.view.show_message("6. Update Seller")
        self.view.show_message("7. Delete Seller")
        self.view.show_message("8. View Sellers")
        self.view.show_message("9. Add Product")
        self.view.show_message("10. Update Product")
        self.view.show_message("11. Delete Product")
        self.view.show_message("12. View Products")
        self.view.show_message("13. Generate Sample Data")
        self.view.show_message("14. Query Top Categories")
        self.view.show_message("15. Query Seller Products")
        self.view.show_message("16. Query Category-Seller Summary")
        self.view.show_message("17. Quit")
        return input("Enter your choice: ")

    def add_category(self):
        name = self.view.get_category_input()
        self.model.add_category(name)
        self.view.show_message("Category added successfully!")

    def update_category(self):
        category_id, name = self.view.get_update_category_input()
        self.model.update_category(category_id, name)
        self.view.show_message("Category updated successfully!")

    def delete_category(self):
        category_id = self.view.get_category_id()
        self.model.delete_category(category_id)
        self.view.show_message("Category deleted successfully!")

    def view_categories(self):
        categories = self.model.get_all_categories()
        self.view.show_categories(categories)

    def add_seller(self):
        name, number = self.view.get_seller_input()
        self.model.add_seller(name, number)
        self.view.show_message("Seller added successfully!")

    def update_seller(self):
        seller_id, name, number = self.view.get_update_seller_input()
        self.model.update_seller(seller_id, name, number)
        self.view.show_message("Seller updated successfully!")

    def delete_seller(self):
        seller_id = self.view.get_seller_id()
        self.model.delete_seller(seller_id)
        self.view.show_message("Seller deleted successfully!")

    def view_sellers(self):
        sellers = self.model.get_all_sellers()
        self.view.show_sellers(sellers)

    def add_product(self):
        name, category_id, seller_id = self.view.get_product_input()
        self.model.add_product(name, category_id, seller_id)
        self.view.show_message("Product added successfully!")

    def update_product(self):
        product_id, name, category_id, seller_id = self.view.get_update_product_input()
        self.model.update_product(product_id, name, category_id, seller_id)
        self.view.show_message("Product updated successfully!")

    def delete_product(self):
        product_id = self.view.get_product_id()
        self.model.delete_product(product_id)
        self.view.show_message("Product deleted successfully!")

    def view_products(self):
        products = self.model.get_all_products()
        self.view.show_products(products)

    def generate_data(self):
        self.model.generate_sample_data()
        self.view.show_message("Sample data generated successfully!")
    
    def query_top_categories(self):
        min_products = int(input("Enter minimum number of products per category: "))
        results, execution_time = self.model.query_top_categories(min_products)
        self.view.show_query_results(results, execution_time)

    def query_seller_products(self):
        seller_id = int(input("Enter seller ID: "))
        results, execution_time = self.model.query_seller_products(seller_id)
        self.view.show_query_results(results, execution_time)

    def query_category_seller_summary(self):
        results, execution_time = self.model.query_category_seller_summary()
        self.view.show_query_results(results, execution_time)
