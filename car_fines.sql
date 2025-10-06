-- Create the database
CREATE DATABASE car_fines;
USE car_fines;

-- Create the fine_records table
CREATE TABLE fine_records (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    vehicle_no VARCHAR(20) UNIQUE,     
    car_model VARCHAR(100),            
    rc_no VARCHAR(50),                 
    driver_name VARCHAR(100),          
    fines DECIMAL(10,2),               
    date DATE                          
);

-- Insert 18 records
INSERT INTO fine_records (vehicle_no, car_model, rc_no, driver_name, fines, date)
VALUES 
('ABC123', 'Toyota Corolla', 'RC123456', 'John Doe', 150.00, '2025-04-18'),
('XYZ789', 'Honda Civic', 'RC987654', 'Jane Smith', 100.00, '2025-04-19'),
('LMN456', 'Ford Mustang', 'RC112233', 'Mike Johnson', 200.00, '2025-04-20'),
('QRS234', 'Chevrolet Malibu', 'RC998877', 'Alice Brown', 250.00, '2025-04-21'),
('DEF567', 'Nissan Altima', 'RC445566', 'James Wilson', 120.00, '2025-04-22'),
('JKL890', 'Hyundai Sonata', 'RC667788', 'Patricia Davis', 90.00, '2025-04-23'),
('MNO123', 'BMW 3 Series', 'RC223344', 'Robert Miller', 180.00, '2025-04-24'),
('PQR456', 'Audi A4', 'RC556677', 'Emily Garcia', 130.00, '2025-04-25'),
('STU789', 'Mercedes-Benz C-Class', 'RC889900', 'David Rodriguez', 220.00, '2025-04-26'),
('VWX012', 'Ford F-150', 'RC112233', 'Sophia Martinez', 160.00, '2025-04-27'),
('YZA345', 'Toyota Camry', 'RC443322', 'William Hernandez', 170.00, '2025-04-28'),
('BCD678', 'Honda Accord', 'RC778899', 'Megan Wilson', 110.00, '2025-04-29'),
('EFG901', 'Chevrolet Silverado', 'RC112244', 'Christopher Lee', 140.00, '2025-04-30'),
('HIJ234', 'Subaru Impreza', 'RC556688', 'Jessica Lewis', 160.00, '2025-05-01'),
('KLM567', 'Mazda 3', 'RC998833', 'Daniel Walker', 200.00, '2025-05-02'),
('NOP890', 'Kia Sorento', 'RC223355', 'Olivia Young', 190.00, '2025-05-03'),
('QRS012', 'Jeep Wrangler', 'RC445577', 'Andrew King', 210.00, '2025-05-04'),
('TUV345', 'Ford Explorer', 'RC667799', 'Charlotte Scott', 180.00, '2025-05-05');

-- Insert 5 more records
INSERT INTO fine_records (vehicle_no, car_model, rc_no, driver_name, fines, date)
VALUES 
('XYZ001', 'Honda CR-V', 'RC223344', 'Lucas Green', 110.00, '2025-05-06'),
('LMN234', 'Toyota RAV4', 'RC556677', 'Rachel Moore', 140.00, '2025-05-07'),
('DEF890', 'Ford Mustang', 'RC889900', 'Matthew Clark', 180.00, '2025-05-08'),
('PQR567', 'Chevrolet Camaro', 'RC998811', 'Isabella Allen', 210.00, '2025-05-09'),
('STU890', 'BMW X5', 'RC112233', 'Henry Turner', 150.00, '2025-05-10');
