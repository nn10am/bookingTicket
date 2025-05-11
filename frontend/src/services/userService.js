import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/v1"

// Function to fetch all users (Admin only)
export const getUsers = async (token) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/users`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.error("API error: ", error);
        return null;
    }
}