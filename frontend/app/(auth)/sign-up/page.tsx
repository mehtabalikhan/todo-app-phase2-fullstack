import SignUpForm from '@/components/auth/sign-up-form';

export default function SignUpPage() {
  return (
    <div>
      <div className="text-center">
        <h2 className="mt-6 text-3xl font-extrabold text-gray-900">Create an account</h2>
      </div>
      <SignUpForm />
    </div>
  );
}