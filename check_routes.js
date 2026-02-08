// Script to check if Next.js routes are properly recognized
const fs = require('fs');
const path = require('path');

console.log('Checking Next.js route structure...');

const frontendDir = 'F:\\todo_app_phase 2\\frontend';

// Check app directory structure
const appDir = path.join(frontendDir, 'app');
if (fs.existsSync(appDir)) {
  console.log('App directory exists');
  const items = fs.readdirSync(appDir);
  console.log('Items in app/:', items);

  // Check for auth routes
  const authDir = path.join(appDir, '(auth)');
  if (fs.existsSync(authDir)) {
    console.log('(auth) directory exists');
    const authItems = fs.readdirSync(authDir);
    console.log('Items in (auth)/:', authItems);

    const signInDir = path.join(authDir, 'sign-in');
    if (fs.existsSync(signInDir)) {
      console.log('sign-in directory exists');
      const signInItems = fs.readdirSync(signInDir);
      console.log('Items in sign-in/:', signInItems);
    }

    const signUpDir = path.join(authDir, 'sign-up');
    if (fs.existsSync(signUpDir)) {
      console.log('sign-up directory exists');
      const signUpItems = fs.readdirSync(signUpDir);
      console.log('Items in sign-up/:', signUpItems);
    }
  }

  // Check if there are alternative auth routes
  const directAuthDirs = ['signin', 'signup', 'login', 'register'].filter(dir => {
    const fullPath = path.join(appDir, dir);
    return fs.existsSync(fullPath);
  });

  if (directAuthDirs.length > 0) {
    console.log('Alternative auth directories found:', directAuthDirs);
  }
} else {
  console.log('App directory does not exist at expected location');
}

console.log('\nNext.js App Router Route Groups:');
console.log('- Route groups in parentheses like (auth) are used for organization');
console.log('- They don\'t affect the URL path structure');
console.log('- /auth/sign-in should map to app/(auth)/sign-in/page.tsx');
console.log('- Make sure you\'re using Next.js 13+ with App Router');