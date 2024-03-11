# Reset Password Example

In case you forget your password, Giza provides a secure and straightforward way to reset it. The process involves two main steps:

## Request a Reset Token

The first step is to request a reset token. This token will be sent to your registered email address. You can request a reset token by running the following command:

```console
> giza request-reset-password-token --email your_email@example.com

[giza][2023-08-30 12:53:18.423] Password recovery email sent
[giza][2023-08-30 12:53:18.428] Please check your email for a password reset token 📬
```

The reset token is a unique string of characters that is used to verify your identity and allow you to change your password. It is only valid for a short period of time for security reasons. If you do not use it within this time, you will need to request a new one.

## Reset Password

Once you have received your reset token, you can use it to reset your password. Run the following command, replacing `your_reset_token` with the token you received in your email:

```console
> giza reset-password --token your_reset_token

Please enter your new password 🔑: # Your new password goes here
Please confirm your new password 🔑:
[giza][2023-08-30 12:55:32.128] Password updated successfully
[giza][2023-08-30 12:55:32.132] Password reset was successful 🎉
```

With the above steps, you have successfully reset your password. Remember, it's important to keep your password secure and not share it with anyone. If you suspect that your password has been compromised, repeat the steps above to reset it.

In case you encounter any issues or need further assistance, feel free to reach out to our support team. We're here to help!

Stay secure! 🔒
