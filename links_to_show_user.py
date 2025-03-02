
import bigbasket as bb
import flipkart as fk
import naturesbasket as nb
import pandas as pd


def show_what(item):

    # Get data from BigBasket
    bb_pop_names, bb_pop_prices, bb_pop_links, bb_cheap_names, bb_cheap_prices, bb_cheap_links = bb.bigbasket(item)

    # Get data from Flipkart
    fk_pop_names, fk_pop_prices, fk_pop_links, fk_cheap_names, fk_cheap_prices, fk_cheap_links = fk.flipkart(item)

    # Get data from Nature's Basket
    nb_pop_names, nb_pop_prices, nb_pop_links, nb_cheap_names, nb_cheap_prices, nb_cheap_links = nb.naturesbasket(item)

    # Combine lists for popular items
    popular_names = bb_pop_names + fk_pop_names + nb_pop_names
    popular_prices = bb_pop_prices + fk_pop_prices + nb_pop_prices
    popular_links = bb_pop_links + fk_pop_links + nb_pop_links

    # Combine lists for cheap items
    cheap_names = bb_cheap_names + fk_cheap_names + nb_cheap_names
    cheap_prices = bb_cheap_prices + fk_cheap_prices + nb_cheap_prices
    cheap_links = bb_cheap_links + fk_cheap_links + nb_cheap_links

    # Create DataFrames
    popular_df = pd.DataFrame({
        'Name': popular_names[:9],
        'Price': popular_prices[:9],
        'Link': popular_links[:9]
    })

    cheap_df = pd.DataFrame({
        'Name': cheap_names[:9],
        'Price': cheap_prices[:9],
        'Link': cheap_links[:9]
    })

    # Ensure 'Price' column is of type string before replacing '₹' symbol
    popular_df['Price'] = popular_df['Price'].astype(str).str.replace('₹', '').astype(float)
    cheap_df['Price'] = cheap_df['Price'].astype(str).str.replace('₹', '').astype(float)

    # Sort DataFrames by Price
    popular_sorted = popular_df.sort_values('Price', ascending=False).reset_index(drop=True)
    cheap_sorted = cheap_df.sort_values('Price', ascending=True).reset_index(drop=True)

    def save_top_two_rows(popular_sorted, cheap_sorted):
        show_user = pd.concat([cheap_sorted.head(3), popular_sorted.head(3)], ignore_index=True)
        return show_user

    show_user = save_top_two_rows(popular_sorted, cheap_sorted)
    show_user.to_csv('show_user.csv', index=False)

show_what("coffee")


