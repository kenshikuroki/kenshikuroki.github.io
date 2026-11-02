module.exports = {
  disableEmoji: true,
  format: "{type}: {subject}",
  maxMessageLength: 64,
  minMessageLength: 3,
  questions: [
    "type",
    "subject",
    //"body",
    //"breaking",
    //"issues",
  ],
  messages: {
    type: "Prefix:",
    subject: "Abstract:",
    //body: "Details (optional):",
    //breaking: "Breaking changes (optional):\n",
    //issues: "Related issues (optional), e.g. #123:",
  },
  scope: [
  ],
  list: [
    "About",
    "Publication",
    "Presentation",
    "Other",
  ],
  types: {
    About: {
      description: "Add/update to the About section",
      value: "About",
    },
    Publication: {
      description: "Add/update to the Publication data",
      value: "Publication",
    },
    Presentation: {
      description: "Add/update to the Presentation data",
      value: "Presentation",
    },
    Other: {
      description: "Other changes",
      value: "Other",
    },
  },
};
