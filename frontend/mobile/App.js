// Login API Stub
const loginApi = async (username, password) => {
    // simulate API call
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (username === 'test' && password === 'password') {
                resolve({ success: true, token: 'abc123' });
            } else {
                reject({ success: false, message: 'Invalid credentials' });
            }
        }, 1000);
    });
};

// Correction API Stub
const correctionApi = async (text) => {
    // simulate API call
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ correctedText: text.replace(/\bteh\b/g, 'the') });
        }, 1000);
    });
};

// Export the API functions
export { loginApi, correctionApi };