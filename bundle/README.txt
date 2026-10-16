FreeMium JayRain — your own audio node
==========================================

This folder has everything your node needs. 5 steps:

1. Install Java 17 or newer (if you don't have it):
   https://adoptium.net

2. Make your node reachable from the internet (pick one):
   EASY: free tunnel at https://playit.gg — create a TCP tunnel
         for port 2333 and note the public address + port.
   ADVANCED: forward port 2333 (TCP) on your router to this PC,
         then use your public IP address.

3. Run the launcher:
   Windows: double-click start-node.bat
   Mac/Linux: double-click (or run) start-node.sh
   On first run it asks you to choose a node password.
   Keep the window open while you want music.

4. Link it to the bot — pick one:
   Dashboard: https://freemiumjayrain.rivaleclipse.dev/setup-wizard
   Discord: run /mynode (or /setupwizard) in any server with the bot.
   You'll enter: your PUBLIC address + port (from step 2)
   and the password you chose in step 3.

5. Done! While this PC is online, your servers get music.
   Tip: turn on "share with my servers" so friends benefit too —
   the more members who link a node, the more reliable music is
   for everyone.

Files in this folder:
  Lavalink.jar        the audio server
  plugins/           youtube + LavaSrc plugins (Spotify, Apple Music, Tidal...)
  application.yml    pre-tuned config (you only set the password)
  start-node.bat     Windows launcher
  start-node.sh      Mac/Linux launcher

Need help? The full illustrated walkthrough is on the dashboard.
