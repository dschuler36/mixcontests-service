from alembic import op


def supabase_user_creation_upgrade():

    # Ensure row level security for users table
    op.execute('ALTER TABLE public.users ENABLE ROW LEVEL SECURITY')

    # Insert into users table whenever a new user signs up with supabase
    op.execute('''
    CREATE FUNCTION public.handle_new_user()
    RETURNS trigger
    LANGUAGE plpgsql
    SECURITY DEFINER
    SET search_path = ''
    AS $$
    BEGIN
        INSERT INTO public.users (id, username, email)
        VALUES (NEW.id, NEW.raw_user_meta_data ->> 'username', NEW.email);
        RETURN NEW;
    END;
    $$;
    ''')

    # Create the trigger to call the function on new user creation
    op.execute('''
    CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();
    ''')


def supabase_user_creation_downgrade():
    # Drop the trigger
    op.execute('DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users')

    # Drop the function
    op.execute('DROP FUNCTION IF EXISTS public.handle_new_user')
