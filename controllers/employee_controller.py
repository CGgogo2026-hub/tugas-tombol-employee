
# controllers/employee_controller.py
from flask import Blueprint, jsonify, request, render_template, redirect
from models.employee_model import employees

employee_bp = Blueprint("employee_bp", __name__)


# READ ALL: GET /employees
@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    return jsonify(employees), 200


# READ ONE: GET /employees/3
@employee_bp.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    for employee in employees:
        if employee["id"] == id:
            return jsonify(employee), 200

    return jsonify({"error": "Not found"}), 404


# FORM TAMBAH EMPLOYEE
@employee_bp.route("/employees/new", methods=["GET"])
def show_form():
    return render_template(
        "form.html",
        employees=employees,
        employee=None
    )


# PROSES TAMBAH EMPLOYEE
@employee_bp.route("/employees/new", methods=["POST"])
def submit_form():
    name = request.form.get("name", "").strip()
    position = request.form.get("position", "Staff").strip()
    salary_text = request.form.get("salary", "0").strip()

    if not name:
        return "Nama wajib diisi!", 400

    try:
        salary = int(salary_text) if salary_text else 0
        if salary < 0:
            return "Gaji tidak boleh negatif!", 400
    except ValueError:
        return "Gaji harus berupa angka!", 400

    new_id = max([e["id"] for e in employees], default=0) + 1

    new_employee = {
        "id": new_id,
        "name": name,
        "position": position or "Staff",
        "salary": salary,
    }

    employees.append(new_employee)

    return redirect("/employees/new")


# FORM UPDATE EMPLOYEE
@employee_bp.route("/employees/<int:id>/update", methods=["GET"])
def show_update_form(id):
    employee = next(
        (e for e in employees if e["id"] == id),
        None
    )

    if employee is None:
        return "Employee tidak ditemukan!", 404

    return render_template(
        "form.html",
        employees=employees,
        employee=employee
    )


# PROSES UPDATE EMPLOYEE
@employee_bp.route("/employees/<int:id>/update", methods=["POST"])
def update_employee(id):
    employee = next(
        (e for e in employees if e["id"] == id),
        None
    )

    if employee is None:
        return "Employee tidak ditemukan!", 404

    name = request.form.get("name", "").strip()
    position = request.form.get("position", "Staff").strip()
    salary_text = request.form.get("salary", "0").strip()

    if not name:
        return "Nama wajib diisi!", 400

    try:
        salary = int(salary_text) if salary_text else 0
        if salary < 0:
            return "Gaji tidak boleh negatif!", 400
    except ValueError:
        return "Gaji harus berupa angka!", 400

    employee["name"] = name
    employee["position"] = position or "Staff"
    employee["salary"] = salary

    return redirect("/employees/new")


# DELETE EMPLOYEE
@employee_bp.route("/employees/<int:id>/delete", methods=["POST"])
def delete_employee(id):
    employee = next(
        (e for e in employees if e["id"] == id),
        None
    )

    if employee is None:
        return "Employee tidak ditemukan!", 404

    employees.remove(employee)

    return redirect("/employees/new")
