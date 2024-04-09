const validateEmail = (email) => {
    const re = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    return re.test(String(email).toLowerCase());
};

const validatePasswordsMatch = (password, confirmPassword) => {
    return password === confirmPassword;
};

export const validateSignupForm = (form) => {
    let errors = {};
    if (!validateEmail(form.email)) {
        errors.email = "Inserir e-mail válido.";
    }
    if (!validatePasswordsMatch(form.password, form.confirmPassword)) {
        errors.confirmPassword = "Senhas não são iguais.";
    }
    return errors;
}

export const validateLoginForm = (form) => {
    let errors = {};
    if (!validateEmail(form.email)) {
        errors.email = "Inserir e-mail válido.";
    }
    return errors;
}