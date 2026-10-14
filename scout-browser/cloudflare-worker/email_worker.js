export default {
  async email(message, env, ctx) {
    const toEmail = message.to.toLowerCase();
    const fromEmail = message.from.toLowerCase();
    const fromDomain = fromEmail.split("@")[1] || "unknown";
    const subject = message.headers.get("subject") || "(No Subject)";

    const response = await fetch(`${env.SCOUT_BACKEND_URL}/api/privacy/inbound-email`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Scout-Webhook-Secret": env.WEBHOOK_SECRET,
      },
      body: JSON.stringify({
        alias_email: toEmail,
        from_email: fromEmail,
        from_domain: fromDomain,
        subject: subject,
      }),
    });

    const decision = await response.json();

    if (!decision.allow_forward) {
      message.setReject("Alias disabled by Scout Privacy Agent due to data leak.");
      return;
    }

    await message.forward(decision.real_user_email);
  },
};
