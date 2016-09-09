from trello import TrelloClient
import webbrowser


def main():
    webbrowser.open_new('https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Praqma%20Sheetconv&key=72ff9314b2d9e1cca758d131e761117e')
    print("Opening auth website")
    api_token = input("paste the token you receive in here: ")
    print(api_token)
    client = TrelloClient(
        api_key='72ff9314b2d9e1cca758d131e761117e',
        api_secret='a475e69f4a864b6d7d2c729f00a255cefc89194c903d450f8da081ba911b016d',
        token=api_token,
        token_secret='your-oauth-token-secret'
    )
    print (client.list_boards())

    spam = ["bacon", "eggs"]
    board = client.add_board('Test')
    id=board.id
    list=board.add_list('Todo')
    for i in spam:
        list.add_card(name=i,due='2016-06-15 09:00:00')
if __name__ == '__main__':
    main()
