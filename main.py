import work.library as package
import Combine_Interface_with_pandas


Combine_Interface_with_pandas.start_menu()
pril = Combine_Interface_with_pandas.bot_or_pril
if pril == "0":
    Combine_Interface_with_pandas.info_telegram_bot()
    package.create_telegram_bot()
elif pril == "1":
    Combine_Interface_with_pandas.run_app()