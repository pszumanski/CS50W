document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('form').addEventListener('submit', () => send_mail())

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#opened-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  const recipients = document.querySelector('#compose-recipients');
  recipients.value = "";
  recipients.disabled = false;
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  const emails_view = document.querySelector('#emails-view');

  emails_view.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#opened-email').style.display = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
        emails.sort((email1, email2) => email1.timestamp - email2.timestamp)
            .forEach(email => {
              const listedEmail = document.createElement('div');
              listedEmail.classList.add('listed-email');

              listedEmail.innerHTML = `
<span class="bold">${email.sender}     </span> ${email.subject}
<span class="right">${email.timestamp} </span>
`;

              if (email.read) {
                listedEmail.classList.add('read');
              }

              if (mailbox !== 'sent') {
                  const archiveButton = document.createElement('button');
                  archiveButton.classList.add('archive-button');
                  archiveButton.classList.add('right');

                  archiveButton.addEventListener('click', event => {
                      event.stopPropagation();
                      archive_email(email.id, !email.archived)
                  });
                  if (email.archived) {
                      archiveButton.innerText = 'unarchive';
                  } else {
                      archiveButton.innerText = 'archive';
                  }

                  listedEmail.appendChild(archiveButton);
              }

              listedEmail.addEventListener('click', () => open_email(email.id));

              emails_view.append(listedEmail);
            })
    });
}

function send_mail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
  })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
  });

  load_mailbox('sent');
}

function open_email(email_id) {
  const openedEmailView = document.querySelector('#opened-email');

  openedEmailView.innerHTML = ``;

  openedEmailView.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
      .then(response => response.json())
      .then(email => {
        const openedEmail = document.createElement('div');

        openedEmail.classList.add('opened-email');
        openedEmail.innerHTML = `
<div class="email-info">
    <p>From:<span class="bold"> ${email.sender}</span></p>
    <p>To: <span class="bold"> ${email.recipients}</span></p>
    <p>Sent at: <span class="bold"> ${email.timestamp}</span></p>
    <button id="reply-button">Reply</button>
</div>
<hr>
<div class="email-subject">${email.subject}</div>
<div class="email-body">${email.body}</div>
`;

        openedEmailView.append(openedEmail);
        document.querySelector('#reply-button').addEventListener('click',() => reply(email))
      });

  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
}

function archive_email(email_id, shouldArchive) {
    fetch(`emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: shouldArchive
        })
    })
    .then(() => load_mailbox('inbox'));
}

function reply(email) {
    console.log(email);
    compose_email();

    const recipients = document.querySelector('#compose-recipients');
    recipients.value = email.sender;
    recipients.disabled = true;

    let subject = email.subject;
    if (subject.slice(0, 4) !== 'Re: ') {
        subject = 'Re: ' + subject;
    }

    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:
    "${email.body}"`;
}