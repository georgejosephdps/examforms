import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF



# --- Utility Functions ---
def number_to_words(n):
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    if n == 0: return "Zero"
    def helper(n):
        if n >= 1000: return helper(n // 1000) + " Thousand " + helper(n % 1000)
        if n >= 100: return helper(n // 100) + " Hundred " + helper(n % 100)
        if n >= 20: return tens[n // 10] + (" " + units[n % 10] if n % 10 != 0 else "")
        if n >= 10: return teens[n - 10]
        return units[n]
    return helper(int(n)).strip() + " Only"



# --- Unique RECEIPT No.

def get_next_receipt_no():
    save_path = 'z:/formdata/registrations.csv'
    if os.path.exists(save_path):
        try:
            df = pd.read_csv(save_path)
            # Count existing rows and add 1
            next_no = len(df) + 1
        except:
            next_no = 1
    else:
        next_no = 1
    
    # Format: DPS-YEAR-001
    year = datetime.now().year
    return f"DPS-{year}-{next_no:03d}"





# --- Printing PDF

def generate_pdf(student_data, selected_exams_df, total, total_words, receipt_no):
    pdf = FPDF()
    pdf.add_page()
    pdf.rect(5, 5, 200, 287) 
    
    try:
        pdf.image('dpsnewlogo.png', x=80, y=10, w=50)
    except:
        pass

    
    pdf.set_y(45)
    #pdf.set_font("Arial", 'B', 16)
    #pdf.cell(190, 10, "DELHI PUBLIC SCHOOL, INDORE", ln=True, align='C')
    

    # Display Receipt Number
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 8, f"Receipt No: {receipt_no}", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 8, "EXAMINATION REGISTRATION RECEIPT", ln=True, align='C')
    pdf.ln(5)
    
    # ... [Rest of your Student & Parent Info code remains the same] ...
    # (Ensure you keep the Parent Name and Mobile logic from the previous step)



    # --- 4. Student & Parent Information ---
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 8, " STUDENT & FAMILY DETAILS", border=1, ln=True, fill=True)
    
    pdf.set_font("Arial", '', 10)
    # Row 1: Student & Scholar No
    pdf.cell(35, 8, " Student Name:", border='LTB')
    pdf.cell(60, 8, f"{student_data['student_name']}", border='RTB')
    pdf.cell(35, 8, " Scholar No:", border='LTB')
    pdf.cell(60, 8, f"{student_data['scholar_No']}", border='RTB', ln=True)
    
    # Row 2: Class & Date
    pdf.cell(35, 8, " Class / Sec:", border='LTB')
    pdf.cell(60, 8, f"{student_data['class']} / {student_data['section']}", border='RTB')
    pdf.cell(35, 8, " Reg. Date:", border='LTB')
    pdf.cell(60, 8, f"{datetime.now().strftime('%d-%b-%Y')}", border='RTB', ln=True)
    
    # Row 3: Father Details
    pdf.cell(35, 8, " Father's Name:", border='LTB')
    pdf.cell(60, 8, f"{student_data['father_name']}", border='RTB')
    pdf.cell(35, 8, " Father Mob:", border='LTB')
    pdf.cell(60, 8, f"{student_data['father_mob']}", border='RTB', ln=True)

    # Row 4: Mother Details
    pdf.cell(35, 8, " Mother's Name:", border='LTB')
    pdf.cell(60, 8, f"{student_data['mother_name']}", border='RTB')
    pdf.cell(35, 8, " Mother Mob:", border='LTB')
    pdf.cell(60, 8, f"{student_data['mother_mob']}", border='RTB', ln=True)
    
    pdf.ln(8)
    
    # --- 5. Exam Table ---
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(140, 10, " Exam Description", border=1, fill=True)
    pdf.cell(50, 10, " Amount (INR)", border=1, ln=True, align='C', fill=True)
    
    pdf.set_font("Arial", '', 11)
    for _, row in selected_exams_df.iterrows():
        pdf.cell(140, 10, f" {row['exam_name']}", border=1)
        pdf.cell(50, 10, f"{row['exam_fee']}.00", border=1, ln=True, align='C')
        
    # Total
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(140, 10, " GRAND TOTAL", border=1, align='R')
    pdf.cell(50, 10, f"Rs. {total}.00", border=1, ln=True, align='C')
    
    # Amount in Words
    pdf.ln(5)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(190, 8, f"Amount in words: Rupees {total_words}")
    
    # --- 6. Signatures ---
    pdf.set_y(-40)
    pdf.set_font("Arial", 'I', 9)
    pdf.cell(95, 10, "__________________________", ln=False, align='C')
    pdf.cell(95, 10, "__________________________", ln=True, align='C')
    pdf.cell(95, 5, "Authorized Signatory", ln=False, align='C')
    pdf.cell(95, 5, "Parent Signature", ln=True, align='C')
    
    return bytes(pdf.output())



    
# --- Page Config ---
st.set_page_config(page_title="Exam Registration System", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    # Ensure these files are in the same folder as this script
    students = pd.read_excel('stud_data.xlsx')
    options = pd.read_excel('options.xlsx')
#    students = pd.read_csv('stud_data.xlsx - Sheet1.csv')
#    options = pd.read_csv('options.xlsx - Sheet1.csv')
    students['scholar_No'] = students['scholar_No'].astype(str)
    return students, options

students_df, options_df = load_data()

st.title("📋 Exam Registration Form")
st.markdown("---")

# --- Student Section ---
st.header("1. Student Details")
scholar_no = st.text_input("Enter Scholar No:", placeholder="e.g. 4639").strip()

student_info = students_df[students_df['scholar_No'] == scholar_no]
col1, col2 = st.columns(2)

if not student_info.empty:
    student = student_info.iloc[0]
    st.session_state['current_student'] = student
    name = col1.text_input("Name", value=student['student_name'], disabled=True)
    class_sec = col2.text_input("Class/Section", value=f"{student['class']} / {student['section']}", disabled=True)
    f_name = col1.text_input("Father Name", value=student['father_name'], disabled=True)
    f_mob = col2.text_input("Father Mobile", value=student['father_mob'], disabled=True)
    m_name = col1.text_input("Mother Name", value=student['mother_name'], disabled=True)
    m_mob = col2.text_input("Mother Mobile", value=student['mother_mob'], disabled=True)
else:
    st.session_state['current_student'] = None
    col1.text_input("Name", value="", placeholder="Auto-filled", disabled=True)
    col2.text_input("Class/Section", value="", placeholder="Auto-filled", disabled=True)
    if scholar_no:
        st.warning("Scholar Number not found.")

st.markdown("---")




# --- Exam Section ---
st.header("2. Exam Selections")

# Initialize a list to store names of exams that are checked
selected_exams = []

st.write("Please select the exams:")

# Create layout: you can use columns to make the checkbox list look cleaner
exam_list = options_df['exam_name'].tolist()
cols = st.columns(3)  # Adjust the number 3 to change how many columns of checkboxes you see

for index, exam in enumerate(exam_list):
    # This distributes checkboxes across the columns
    with cols[index % 3]: 
        if st.checkbox(exam, key=f"chk_{exam}"):
            selected_exams.append(exam)

total_amount = 0
if selected_exams:
    # Filter the dataframe based on the checkbox selections
    invoice_data = options_df[options_df['exam_name'].isin(selected_exams)][['exam_name', 'exam_fee']]
    
    st.markdown("---")
    st.subheader("Invoice Summary")
    st.table(invoice_data)
    
    total_amount = invoice_data['exam_fee'].sum()
    st.markdown(f"### Total: ₹ {total_amount}")
    st.info(f"**Amount in Words:** {number_to_words(total_amount)}")
else:
    st.info("Select at least one exam to see the invoice summary.")

st.markdown("---")




# --- Updated Save Logic ---
col_btn1, col_btn2, _ = st.columns([1, 1, 4])

with col_btn1:
    if st.button("SUBMIT / SAVE", type="primary"):
        if not scholar_no or not selected_exams or st.session_state['current_student'] is None:
            st.error("Please ensure Scholar No is valid and exams are selected.")
        else:
            # Generate the Unique Receipt Number
            receipt_no = get_next_receipt_no()
            
            save_directory = 'z:/formdata'
            full_path = os.path.join(save_directory, 'registrations.csv')
            
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            
            # Prepare data row with Receipt No
            new_entry = {
                "Receipt No": receipt_no,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Scholar No": scholar_no,
                "Student Name": st.session_state['current_student']['student_name'],
                "Class": st.session_state['current_student']['class'],
                "Exams": ", ".join(selected_exams),
                "Total Amount": total_amount
            }
            
            df_new = pd.DataFrame([new_entry])
            
            try:
                if not os.path.isfile(full_path):
                    df_new.to_csv(full_path, index=False)
                else:
                    df_new.to_csv(full_path, mode='a', header=False, index=False)
                
                st.success(f"Saved! Receipt No: {receipt_no}")
                
                # Store receipt_no in session state so the download button can use it
                st.session_state['last_receipt_no'] = receipt_no
                
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Updated Download Button ---
    if 'last_receipt_no' in st.session_state and selected_exams:
        current_receipt = st.session_state['last_receipt_no']
        pdf_bytes = generate_pdf(
            st.session_state['current_student'], 
            invoice_data, 
            total_amount, 
            number_to_words(total_amount),
            current_receipt
        )
        
        st.download_button(
            label="📄 DOWNLOAD PDF RECEIPT",
            data=pdf_bytes,
            file_name=f"Receipt_{current_receipt}.pdf",
            mime="application/pdf"
        )





with col_btn2:
    if st.button("CLEAR / CANCEL"):
        st.rerun()

# --- View Saved Data ---
with st.expander("📂 View All Saved Registrations"):
    save_path = 'z:/formdata/registrations.csv'
    if os.path.isfile(save_path):
        saved_df = pd.read_csv(save_path)
        st.dataframe(saved_df)
    else:
        st.write("No registrations found in the specified path.")





# --- 7. Search & Re-print Section ---
st.markdown("---")
st.header("🔍 Search & Re-print Receipts")

search_query = st.text_input("Search by Scholar No or Receipt No:", placeholder="e.g. 4639 or DPS-2025-001").strip()

if search_query:
    save_path = 'z:/formdata/registrations.csv'
    if os.path.exists(save_path):
        all_data = pd.read_csv(save_path)
        
        # Filter data based on search
        results = all_data[(all_data['Scholar No'].astype(str) == search_query) | 
                          (all_data['Receipt No'].astype(str) == search_query)]
        
        if not results.empty:
            st.success(f"Found {len(results)} record(s):")
            for i, row in results.iterrows():
                with st.expander(f"Receipt: {row['Receipt No']} - {row['Student Name']}"):
                    col_a, col_b = st.columns(2)
                    col_a.write(f"**Date:** {row['Timestamp']}")
                    col_a.write(f"**Class:** {row['Class']}")
                    col_b.write(f"**Exams:** {row['Exams']}")
                    col_b.write(f"**Total:** ₹{row['Total Amount']}")
                    
                    # Re-generate PDF for this specific row
                    # We fetch the full student info from the main dataframe to get parent details
                    orig_student = students_df[students_df['scholar_No'] == str(row['Scholar No'])]
                    
                    if not orig_student.empty:
                        # Prepare exam data for the table
                        # Since the CSV stores exams as a string, we reconstruct a mini-dataframe
                        exam_list_str = row['Exams'].split(", ")
                        reprint_invoice_data = options_df[options_df['exam_name'].isin(exam_list_str)]
                        
                        pdf_reprint = generate_pdf(
                            orig_student.iloc[0],
                            reprint_invoice_data,
                            row['Total Amount'],
                            number_to_words(row['Total Amount']),
                            row['Receipt No']
                        )
                        
                        st.download_button(
                            label=f"📥 Download Copy of {row['Receipt No']}",
                            data=pdf_reprint,
                            file_name=f"Copy_{row['Receipt No']}.pdf",
                            mime="application/pdf",
                            key=f"reprint_{row['Receipt No']}" # Unique key for each button
                        )
        else:
            st.error("No records found matching that ID.")
    else:
        st.info("No registration database found yet.")

