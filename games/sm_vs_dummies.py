from war import SimpleMindedPlayer, DummiePlayer, play_game
play_game([SimpleMindedPlayer()] + [DummiePlayer() for _ in range(12)])
