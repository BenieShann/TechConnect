from app import create_app
from app.routes import Routes

app = create_app()

# if __name__ == "__main__":    
#     app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
    
        page_controller = Routes(app)
        app.run(debug=True, port=8005)
        
    