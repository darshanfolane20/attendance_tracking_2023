import streamlit as st
conn = st.experimental_connection('snowflake', type='sql')
def verify_code(verification_code):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM EMP WHERE code = '{verification_code}' AND attended = FALSE")
    attendee_data = cursor.fetchone()
    if attendee_data:
        cursor.execute(f"UPDATE EMP SET attended = TRUE WHERE code = '{verification_code}'")
        conn.commit()
        return True
    else:
        return False
st.title('Event Attendance Verification')
verification_code = st.text_input('Enter Verification Code:')
if st.button('Verify'):
    if verification_code:
        if verify_code(verification_code):
            st.success('Code verified successfully! Attendance count increased.')
        else:
            st.error('Invalid code or code already used.')
# Display attendance count
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM EMP WHERE attended = TRUE")
attendance_count = cursor.fetchone()[0]
st.write(f'Total Attended: {attendance_count}')
