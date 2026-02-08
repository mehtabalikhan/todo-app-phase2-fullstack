import SignInForm from '@/components/auth/sign-in-form';

export default function SignInPage() {
  return (
    <div>
      <div className="text-center">
        <h2 className="mt-6 text-3xl font-extrabold text-gray-900">Sign in to your account</h2>
      </div>
      <SignInForm />
    </div>
  );
}