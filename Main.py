import random
from flask import Flask, request, jsonify
from io import BytesIO
import psutil

import requests
from flask import Flask, render_template, request, send_file
from flask_caching import Cache
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL import Image, ImageDraw, ImageFont, ImageOps
from flask import Flask, render_template_string, send_file, request
from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
import requests
import datetime
from io import BytesIO
import numpy as np

shape_position = (50, 100)
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

red = (255, 0, 0)
yellow = (255, 255, 0)
orange = (255, 165, 0)
pink = (255, 192, 203)
aqua = (0, 255, 255)
dark_green = (0, 100, 0)
white = (255, 255, 255)
light_green = (144, 238, 144)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rank/<name>/<rank_type>')
def generate_rank_image(name, rank_type):
    try:
        # Extract avatar URL from query parameters
        avatar_url = request.args.get('pfp')

        # Determine rank text and color based on rank type
        if rank_type.lower() == 'cat+':
            rank_text = "Cat+"
            rank_color1 = "purple"
            rank_color2 = "white"
            background_url = random.choice([
                'https://wallpapercave.com/wp/wp5171323.jpg',
                'https://wallpapercave.com/wp/wp2057070.jpg',
                # Add more background URLs for "Cat+" rank
            ])
        else:
            rank_text = rank_type
            rank_color1 = "blue"
            rank_color2 = "white"
            background_url = 'https://i.ibb.co/Bwrb0Cv/imageedit-2-6515667300.jpg'  # Default background URL

        # Open and resize background image
        background_response = requests.get(background_url)
        background_response.raise_for_status()
        background = Image.open(BytesIO(background_response.content)).convert("RGBA")
        background = background.resize((600, 202))

        # Create drawing context
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("arial.ttf", 28)  # Adjust font and size as needed

        # Blur the background image
        blur_radius = 5
        blurred_background = background.filter(ImageFilter.GaussianBlur(blur_radius))

        # Draw rank text on blurred background
        draw_blurred = ImageDraw.Draw(blurred_background)
        draw_blurred.text((180, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color1)
        draw_blurred.text((175, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color2)

        # Draw main text on original background
        draw.text((180, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color1)
        draw.text((175, 70), f"This is your rank: {rank_text}", font=font, fill=rank_color2)

        # Add additional text and quotes for "Cat+" rank
        if rank_type.lower() == 'cat+':
            # Fetch a quote from the quotable.io API
            quote_api_url = 'https://api.quotable.io/quotes/random?maxLength=40'
            quote_response = requests.get(quote_api_url)
            quote_response.raise_for_status()  # Ensure the request was successful

            # Parse JSON response
            quote_data = quote_response.json()

            if isinstance(quote_data, list) and len(quote_data) > 0:
                # Access the content inside the first element of the list
                quote_text = quote_data[0].get('content', '')
            else:
                quote_text = 'We can win'

            # Draw the quote text on the blurred background
            draw_blurred.text((5, 170), f'"{quote_text}"', font=font, fill="green")
            draw_blurred.text((0, 170), f'"{quote_text}"', font=font, fill="white")

            # Draw additional text
            draw_blurred.text((180, 100), "🎮 GG ezy Your the best!", font=font, fill="blue")
        else:
            # Draw additional text for non-"Cat+" ranks
            draw_blurred.text((180, 100), "Good job enjoy your perks!", font=font, fill="blue")

        # Open and paste avatar onto blurred background
        avatar_response = requests.get(avatar_url)
        avatar_response.raise_for_status()
        avatar = Image.open(BytesIO(avatar_response.content))
        avatar = avatar.resize((120, 120))
        blurred_background.paste(avatar, (30, 35))  # Adjust position as needed

        # Save the resulting image
        image_buffer = BytesIO()
        blurred_background.save(image_buffer, format='PNG')
        image_buffer.seek(0)

        # Return the image file
        return send_file(image_buffer, mimetype='image/png')

    except Exception as e:
        print(e)
        return "An error occurred while generating the rank image.", 500




@app.route('/vod/<username>/<interval>/<mode>')
def generate_bedwars_image22(username, interval, mode):
    try:
        additional_info_url = f"https://stats.pika-network.net/api/profile/{username}/"
        additional_info_response = requests.get(additional_info_url)

        if additional_info_response.status_code == 200:
            additional_data = additional_info_response.json()
            special_value_username = additional_data.get("username", None)

            if special_value_username:
                bedwars_stats_url = f"https://stats.pika-network.net/api/profile/{special_value_username}/leaderboard?type=bedwars&interval={interval}&mode={mode}"
                bedwars_stats_response = requests.get(bedwars_stats_url)

                if bedwars_stats_response.status_code == 200:
                    pika_data = bedwars_stats_response.json()
                    result_image = generate_bedwars_image22(username, interval, mode, pika_data, additional_data, special_value_username)

                    image_buffer = BytesIO()
                    result_image.save(image_buffer, format='PNG')
                    image_buffer.seek(0)

                    return send_file(image_buffer, mimetype='image/png')
                else:
                    return "Failed to fetch Bed Wars stats.", 500
            else:
                return f"Failed to fetch special value username for {username}.", 500
        else:
            return f"Failed to fetch additional information for {username}.", 500

    except Exception as e:
        print(e)
        return f"🏳️‍⚧️ An error occurred ❌ ., 🛠️ Zumi Bot api Version V1 : Loaded failure noted as {e}", 500

def generate_bedwars_image22(username, interval, mode, pika_data, additional_data, special_value_username):
    # Create a blank transparent image
    result_image = Image.new('RGBA', (1280, 720), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(result_image)

    # Overlay image
    idk_image_url = 'https://i.ibb.co/SsN6TFW/alpha2fgsdg-1-Bedwars-sidktats.png'
    idk_image = Image.open(BytesIO(requests.get(idk_image_url).content)).convert('RGBA')
    idk_image = idk_image.resize((1280, 720), resample=Image.LANCZOS)
    result_image.paste(idk_image, (0, 0), idk_image)

    # Add skin to the image if available
    skin_url = f"https://visage.surgeplay.com/full/512/{username}"
    headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
    skin_response = requests.get(skin_url, stream=True, headers=headers)

    if skin_response.status_code == 200:
        skin_image = Image.open(BytesIO(skin_response.content)).convert('RGBA')
        skin_image = skin_image.resize((300, 500), resample=Image.LANCZOS)
        result_image.paste(skin_image, (950, 10), skin_image)
    else:
        # Use default skin image
        default_skin_image = Image.open("default_skin.png").convert('RGBA')
        default_skin_image = default_skin_image.resize((220, 500), resample=Image.LANCZOS)
        result_image.paste(default_skin_image, (980, 10), default_skin_image)

    if additional_data.get("discord_verified"):
        discord_icon_url = "https://th.bing.com/th/id/R.5ff232157d19b921f7dc016519e3c577?rik=qQzQh7EIMFt0sg&pid=ImgRaw&r=0"
        discord_icon = Image.open(BytesIO(requests.get(discord_icon_url).content)).convert('RGBA')
        discord_icon = discord_icon.resize((35, 35), resample=Image.LANCZOS)
        result_image.paste(discord_icon, (995, 645), discord_icon)

    if additional_data.get("email_verified"):
        email_icon_url = "https://logos-world.net/wp-content/uploads/2020/11/Gmail-Logo.png"
        email_icon = Image.open(BytesIO(requests.get(email_icon_url).content)).convert('RGBA')
        email_icon = email_icon.resize((35, 25), resample=Image.LANCZOS)
        result_image.paste(email_icon, (950, 650), email_icon)

    skin_url2 = f"https://visage.surgeplay.com/face/512/{special_value_username}"
    headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
    skin_response2 = requests.get(skin_url2, stream=True, headers=headers)

    print("Head Image API Response Status Code:", skin_response2.status_code)  # Debugging line

    if additional_data.get("ranks"):
      rank_display_name = additional_data["ranks"][0].get("displayName", "N/A")
      rank_level = additional_data["ranks"][0].get("level", 0)

      # Define colors based on rank
      if rank_display_name == "Vip":
          rank_color = "green"
      elif rank_display_name == "Elite":
          rank_color = "lightblue"  # You mentioned light aqua, lightblue is closer
      elif rank_display_name == "Titan":
          rank_color = "yellow"
      else:
          rank_color = "white"  # Default color if rank not specified

      draw.text((395, 45), f": {rank_display_name}", fill=rank_color, font=ImageFont.truetype("mine.ttf", 40))
    else:
      print("No ranks found")


    if skin_response2.status_code == 200:
        skin_image2 = Image.open(BytesIO(skin_response2.content)).convert('RGBA')
        skin_image = skin_image2.resize((45, 45), resample=Image.LANCZOS)
        result_image.paste(skin_image, (20, 50), skin_image)
        # Save the image locally for inspection
        skin_image2.save("head_image.png")  # Debugging line
    else:
        print("Failed to retrieve head image.")  # Debugging line

    # Drawing text and statistic\


    draw.text((75, 45), f"| {username.replace('_', ' ').capitalize()} ", fill='white', font=ImageFont.truetype("mine.ttf", 40))


    draw.text((600, 650), f"({mode.replace('_', ' ').lower()}) ({interval.lower().capitalize()})", fill='white', font=ImageFont.truetype("mine.ttf", 20))
    rank_level = additional_data["rank"].get("level", "N/A")

    stat_positions = [
        ("Wins", get_entry_value(pika_data, "Wins"), (100, 200)),
        ("Losses", get_entry_value(pika_data, "Losses"), (410, 200)),
        ("Final deaths", get_entry_value(pika_data, "Final deaths"), (417, 320)),
        ("Final kills", get_entry_value(pika_data, "Final kills"), (85, 320)),
        ("Beds broken", get_entry_value(pika_data, "Beds destroyed"), (87, 565)),
        ("Beds lost", get_entry_value(pika_data, "Losses"), (412, 565)),
        ("Kills", get_entry_value(pika_data, "Kills"), (85, 440)),
        ("Deaths", get_entry_value(pika_data, "Deaths"), (405, 440)),
    ]



    for stat_name, stat_value, position in stat_positions:
        draw.text(position, f"{stat_value}", fill='white', font=ImageFont.truetype("arial.ttf", 40))

    highest_winstreak_value = get_entry_value(pika_data, "Highest winstreak reached")
    draw.text((735, 440), f"{highest_winstreak_value}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    # Api section

    final_deaths = int(get_entry_value(pika_data, "Final deaths"))
    final_kills = int(get_entry_value(pika_data, "Final kills"))
    final_kill_to_death_ratio = final_kills / final_deaths if final_deaths > 0 else final_kills
    draw.text((725, 320), f"{final_kill_to_death_ratio:.2f}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    wins = int(get_entry_value(pika_data, "Wins"))
    losses = int(get_entry_value(pika_data, "Losses"))
    win_to_loss_ratio = wins / losses if losses > 0 else wins
    draw.text((735, 200), f"{win_to_loss_ratio:.2f}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    games_played = get_entry_value(pika_data, "Games played")
    draw.text((730, 565), f"{games_played}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    if additional_data.get("clan"):
        clan_name = additional_data["clan"].get("name", "No Clan")
        draw.text((950, 570), f"{clan_name}", fill='purple', font=ImageFont.truetype("mine.ttf", 36))
    else:
        draw.text((960, 570), "No Guild", fill='white', font=ImageFont.truetype("mine.ttf", 40))

    if additional_data.get("rank"):
        rank_level = additional_data["rank"].get("level", "N/A")
        draw.text((950, 610), f"Network Level: @{rank_level}", fill='pink', font=ImageFont.truetype("mine.ttf", 26))
    else:
        draw.text((950, 610), "No Levels Found!", fill='red', font=ImageFont.truetype("mine.ttf", 26))

    return result_image


background_font = ImageFont.truetype("arial.ttf", 24)
level_font = ImageFont.truetype("arial.ttf", 20)

def draw_rounded_rectangle(draw, position, size, color, radius):
  x, y = position
  width, height = size
  draw.rectangle([x, y + radius, x + width, y + height - radius], fill=color)
  draw.rectangle([x + radius, y, x + width - radius, y + height], fill=color)
  draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
  draw.pieslice([x + width - radius * 2, y, x + width, y + radius * 2], 270, 360, fill=color)
  draw.pieslice([x, y + height - radius * 2, x + radius * 2, y + height], 90, 180, fill=color)
  draw.pieslice([x + width - radius * 2, y + height - radius * 2, x + width, y + height], 0, 90, fill=color)

def draw_progress_bar(draw, position, size, progress, color):
  x, y = position
  width, height = size
  progress_width = int(width * progress)
  draw.rectangle([x, y, x + progress_width, y + height], fill=color)

@app.route('/lvls/<int:level>/<int:messages>/<guild_name>')
def generate_level_image(level, messages, guild_name):
  try:
      # Create a blank image with the specified dimensions
      image_width = 600
      image_height = 200
      background_color = (54, 57, 63)  # Discord background color
      background = Image.open("backgb2.png")  # Load custom background image
      background = background.resize((image_width, image_height))  # Resize background image

      # Create a drawing context
      draw = ImageDraw.Draw(background)
      font = ImageFont.truetype("arial.ttf", 20)  # Adjust font and size as needed

      # Add guild name text at the top
      guild_text = f"AKA {guild_name}"
      guild_text_bbox = draw.textbbox((0, 0), guild_text, font=font)
      guild_text_width = guild_text_bbox[2] - guild_text_bbox[0]
      draw.text((430, 180), guild_text, fill=(255, 255, 255), font=font)

      # Load user avatar
      avatar_url = request.args.get('pfp')
      if avatar_url:
          avatar_response = requests.get(avatar_url)
          if avatar_response.status_code == 200:
              avatar_image = Image.open(BytesIO(avatar_response.content)).convert('RGBA')
              avatar_size = (150, 150)  # Larger avatar size
              avatar_image = avatar_image.resize(avatar_size, resample=Image.LANCZOS)
              background.paste(avatar_image, (430, 20), avatar_image)

      # Add level, messages, and progress bar inside a rectangle
      rectangle_position = (20, 20)  # Adjusted position
      rectangle_size = (image_width - 50 - avatar_size[0], 160)  # Adjusted size
      rectangle_color = (32, 34, 37)  # Dark grey color
      draw_rounded_rectangle(draw, rectangle_position, rectangle_size, rectangle_color, 10)

      # Add level text
      level_text = f"Level: {level}"
      draw.text((rectangle_position[0] + 20, 50), level_text, fill=(255, 255, 255), font=font)

      # Add messages text
      messages_text = f"Messages: {messages}"
      draw.text((rectangle_position[0] + 20, 80), messages_text, fill=(255, 255, 255), font=font)

      # Draw progress bar
      progress_bar_position = (rectangle_position[0] + 20, 100)  # Adjusted position
      progress_bar_size = (rectangle_size[0] - 40, 20)  # Adjusted size
      progress_color = (114, 137, 218)  # Discord accent color
      progress = min(level / 100, 1.0)
      progressed = 9# Cap progress at 100%
      draw_progress_bar(draw, progress_bar_position, progress_bar_size, progress, progress_color)


      # Add progress text
      progress_text = f"Progress: {progress:.1%}"
      draw.text((rectangle_position[0] + 20, 150), progress_text, fill=(255, 255, 255), font=font)

      # Save the resulting image to a BytesIO buffer
      image_buffer = BytesIO()
      background.save(image_buffer, format='PNG')
      image_buffer.seek(0)

      # Return the image file
      return send_file(image_buffer, mimetype='image/png')

  except Exception as e:
      error_message = f"An error occurred while generating the level image: {str(e)}"
      print(error_message)
      return error_message, 500


@app.route('/bw/vid/<usern>/<interval>/<mode>')
def generate_video(usern, interval, mode):
    try:
        # Load the video file
        video_path = "/well.mp4"
        video_clip = VideoFileClip(video_path)

        # Fetch the image from the API
        image_url = f"http://api.astralaxis.info:35819/vod/{usern}/{interval}/{mode}"
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code != 200:
            return f"Error: Unable to fetch image from API. Status code: {response.status_code}"

        # Save the fetched image
        image = Image.open(BytesIO(response.content))
        image_path = f"image{usern}overlay.png"
        image.save(image_path)

        # Resize the image to match the video's dimensions
        image = image.resize((video_clip.size[0], video_clip.size[1]))

        # Add text overlay
        text = TextClip("Made by Kushi_k", fontsize=70, color='white')
        text = text.set_position(('center', 'bottom')).set_duration(video_clip.duration)

        # Composite the image and text clips over the video
        final_clip = CompositeVideoClip([video_clip, ImageClip(image_path).set_duration(video_clip.duration).set_position(('center', 'center')), text])

        # Write the modified video to a file
        output_path = f"{usern}_this shit took to much time bro.mp4"
        final_clip.write_videofile(output_path, codec='libx264', fps=video_clip.fps)

        # Close the video clip objects
        video_clip.close()
        final_clip.close()

        # Send the modified video file as a response
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/bw/expo/<username>/<interval>/<mode>')
def get_bedwars_exploits(username, interval, mode):
    api_url = f'https://stats.pika-network.net/api/profile/{username}/leaderboard?type=bedwars&interval={interval}&mode={mode}'

    try:
        response = requests.get(api_url)
        data = response.json()

        if 'Games played' in data and 'Wins' in data and 'Losses' in data:
            games_played = int(data['Games played']['entries'][0]['value'])
            wins = int(data['Wins']['entries'][0]['value'])
            losses = int(data['Losses']['entries'][0]['value'])

            hubs = games_played - (wins + losses)

            return jsonify({'username': username, 'exploits': hubs}), 200
        else:
            return jsonify({'error': f'Data not found {api_url}'}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'api_url': api_url}), 500

@app.route('/bw/arr/<username>/<interval>/<mode>', methods=['GET'])
def get_arrows_hit(username, interval, mode):
    api_url = f'https://stats.pika-network.net/api/profile/{username}/leaderboard?type=bedwars&interval={interval}&mode={mode}'

    try:
        response = requests.get(api_url)
        data = response.json()

        if 'Arrows hit' in data:
            arrows_hit = int(data['Arrows hit']['entries'][0]['value'])

            return jsonify({'username': username, 'arrows_hit': arrows_hit}), 200
        else:
            return jsonify({'error': 'Data not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'api_url': api_url}), 500



@app.route('/bw/arrrat/<username>/<interval>/<mode>', methods=['GET'])
def get_arrows_ratio(username, interval, mode):
    api_url = f'https://stats.pika-network.net/api/profile/{username}/leaderboard?type=bedwars&interval={interval}&mode={mode}'

    try:
        response = requests.get(api_url)
        data = response.json()

        if 'Arrows hit' in data and 'Arrows shot' in data:
            arrows_hit = int(data['Arrows hit']['entries'][0]['value'])
            arrows_shot = int(data['Arrows shot']['entries'][0]['value'])

            if arrows_shot != 0:
                ratio = round(arrows_hit / arrows_shot, 3)
            else:
                ratio = 0

            return jsonify({'username': username, 'arrows_ratio': ratio}), 200
        else:
            return jsonify({'error': 'Data not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'api_url': api_url}), 500

@app.route('/sys')
def system_info():
    return render_template('sys.html')

@app.route('/sys/data')
def system_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    ip_address = request.remote_addr

    # Log the IP address
    print(f"{ip_address} has contacted the server")

    return jsonify(cpu_usage=cpu_usage, ram_usage=ram_usage, ip_address=ip_address)



@app.route('/bw/rank/<ign>')
def get_bw_rank(ign):
    url = f"https://stats.pika-network.net/api/profile/{ign}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'ranks' in data:
            ranks_data = data['ranks']
            games_ranks = [rank for rank in ranks_data if rank["name"].startswith("games")]
            if games_ranks:
                latest_rank = max(games_ranks, key=lambda x: x["name"])
                return jsonify({"Ranks": [latest_rank]})
            else:
                return jsonify({"error": "No BedWars rank found for this player Zumi bot Api"}), 404
        else:
            return jsonify({"error": "Ranks data not found for this player"}), 404
    else:
        return jsonify({"error": "Unable to fetch data for this player"}), 404

def get_exploits(username, interval, mode):
  url = f"http://de-prem-01.hosts.optikservers.com:25684/bw/expo/{username}/{interval}/{mode}"
  print("Exploits URL:", url)
  response = requests.get(url)
  return response.json()["exploits"]

def get_arrow_hit(username, interval, mode):
  url = f"http://de-prem-01.hosts.optikservers.com:25684/bw/arr/{username}/{interval}/{mode}"
  print("Arrow Hit URL:", url)
  response = requests.get(url)
  return response.json()["arrows_hit"]

def get_arrow_ratio(username, interval, mode):
  url = f"http://de-prem-01.hosts.optikservers.com:25684/bw/arrrat/{username}/{interval}/{mode}"
  print("Arrow Ratio URL:", url)
  response = requests.get(url)
  return response.json()["arrows_ratio"]

def get_last_seen(username):
  url = f"http://de-prem-01.hosts.optikservers.com:25684/bw/ls/{username}"
  response = requests.get(url)
  data = response.json()

  last_seen_string = data["last_seen"]

  return last_seen_string

def get_rank(special_username):
  response = requests.get(f"http://de-prem-01.hosts.optikservers.com:25684/bw/rank/{special_username}")
  ranks = response.json().get("Ranks", [])
  rank_display_name = "N/A"
  for rank_info in ranks:
      rank_display_name = rank_info.get("displayName", "N/A")
      break
  return rank_display_name

def get_guild_info(username):
  url = f"http://de-prem-01.hosts.optikservers.com:25684/bw/guild/{username}"
  response = requests.get(url)
  data = response.json()

  guild_owner = data["guild_owner"]
  guild_level = data["guild_level"]
  guild_members = data["guild_members"]

  return guild_owner, guild_level, guild_members

@app.route('/bw/<username>/<interval>/<mode>')
def generate_bedwars_image(username, interval, mode):
  try:
      additional_info_url = f"https://stats.pika-network.net/api/profile/{username}/"
      print("Additional Info URL:", additional_info_url)
      additional_info_response = requests.get(additional_info_url)

      if additional_info_response.status_code == 200:
          additional_data = additional_info_response.json()
          special_value_username = additional_data.get("username", None)

          if special_value_username:
              bedwars_stats_url = f"https://stats.pika-network.net/api/profile/{special_value_username}/leaderboard?type=bedwars&interval={interval}&mode={mode}"
              print("Bedwars Stats URL:", bedwars_stats_url)
              bedwars_stats_response = requests.get(bedwars_stats_url)

              if bedwars_stats_response.status_code == 200:
                  pika_data = bedwars_stats_response.json()
                  result_image = generate_bedwars_image(username, interval, mode, pika_data, additional_data, special_value_username)

                  image_buffer = BytesIO()
                  result_image.save(image_buffer, format='PNG')
                  image_buffer.seek(0)

                  return send_file(image_buffer, mimetype='image/png')
              else:
                  return "Failed to fetch Bed Wars stats.", 500
          else:
              return f"Failed to fetch special value username for {username}.", 500
      else:
          return f"Failed to fetch additional information for {username}.", 500

  except Exception as e:
      print(e)
      return f"🏳️‍⚧️ An error occurred ❌ ., 🛠️ Zumi Bot api Version V1 : Loaded failure noted as {e}", 500

def generate_bedwars_image(username, interval, mode, pika_data, additional_data, special_value_username):
  result_image = Image.new('RGBA', (1280, 720), color=(0, 0, 0, 0))
  draw = ImageDraw.Draw(result_image)

  # Background
  if additional_data.get("rank", {}).get("level", 0) >= 6:
      background_urls = [
          'https://wallpaperaccess.com/full/2936972.jpg',  # Japanese Street at Night
          'https://th.bing.com/th/id/R.46e91d3ebbe8ae4642f7bc094310dbd8?rik=fjseaUEGM6tVng&pid=ImgRaw&r=0',
          'https://wallpaperaccess.com/full/4583657.png',

      ]

      random_background_url = random.choice(background_urls)
      background_image = Image.open(BytesIO(requests.get(random_background_url).content)).convert('RGBA')
      print(f"{random_background_url} has been loaded")
      background_image = background_image.resize((1280, 720), resample=Image.LANCZOS)
  else:
      background_image = Image.open("Rise1-0.png").convert('RGBA')
      background_image = background_image.resize((1280, 720), resample=Image.LANCZOS)

  result_image.paste(background_image, (0, 0))

  # Overlay image
  idk_image_url = 'https://i.ibb.co/QC2S1rG/USE-PNG.png'
  idk_image = Image.open(BytesIO(requests.get(idk_image_url).content)).convert('RGBA')
  idk_image = idk_image.resize((1280, 720), resample=Image.LANCZOS)
  result_image.paste(idk_image, (0, 0), idk_image)

  # Add skin to the image if available
  skin_url = f"https://starlightskins.lunareclipse.studio/render/criss_cross/{username}/bust"
  headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
  skin_response = requests.get(skin_url, stream=True, headers=headers)
  skin_url_cracked = f"https://starlightskins.lunareclipse.studio/render/criss_cross/jaidle/bust"
  skin_response_cra = requests.get(skin_url_cracked, stream=True, headers=headers)

  if skin_response.status_code == 200:
      skin_image = Image.open(BytesIO(skin_response.content)).convert('RGBA') 
      print(f"{skin_response} has been loaded")
      
      skin_image = skin_image.resize((247, 270), resample=Image.LANCZOS)
      result_image.paste(skin_image, (950, 174), skin_image)
  else:
      # Use default skin image
      skin_image_cra = Image.open(BytesIO(skin_response_cra.content)).convert('RGBA')
      skin_image_cra = skin_image_cra.resize((247, 270), resample=Image.LANCZOS)
      result_image.paste(skin_image_cra, (950, 174), skin_image_cra)

  if additional_data.get("discord_verified"):
      discord_icon_url = "https://th.bing.com/th/id/R.5ff232157d19b921f7dc016519e3c577?rik=qQzQh7EIMFt0sg&pid=ImgRaw&r=0"
      discord_icon = Image.open(BytesIO(requests.get(discord_icon_url).content)).convert('RGBA')
      discord_icon = discord_icon.resize((75, 75), resample=Image.LANCZOS)
      result_image.paste(discord_icon, (1047, 5), discord_icon)

  if additional_data.get("email_verified"):
      email_icon_url = "https://logos-world.net/wp-content/uploads/2020/11/Gmail-Logo.png"
      email_icon = Image.open(BytesIO(requests.get(email_icon_url).content)).convert('RGBA')
      email_icon = email_icon.resize((85, 45), resample=Image.LANCZOS)
      result_image.paste(email_icon, (915, 25), email_icon)
  
  if additional_data.get("discord_boosting"):
    email_icon_url = "https://cdn.iconscout.com/icon/free/png-256/free-level-discord-boost-6745736-5575059.png"
    email_icon = Image.open(BytesIO(requests.get(email_icon_url).content)).convert('RGBA')
    email_icon = email_icon.resize((75, 75), resample=Image.LANCZOS)
    result_image.paste(email_icon, (1175, 5), email_icon)
    
   

  skin_url2 = f"https://visage.surgeplay.com/face/512/{special_value_username}"
  headers = {'User-Agent': 'Zumi/1.0 (+http://zumi.42web.io/?i=1; Nadhilaplayz@gmail.com)'}
  skin_response2 = requests.get(skin_url2, stream=True, headers=headers)

  print("Head Image API Response Status Code:", skin_response2.status_code)  # Debugging line


  rank_display_name = get_rank(special_value_username)
  if rank_display_name == "VIP":
      rank_color = "green"
      draw.text((225, 35), f"{special_value_username}", fill=rank_color, font=ImageFont.truetype("mine.ttf", 40))
      username_position = (115, 40)
  elif rank_display_name == "Elite":
      rank_color = "lightblue"  
      draw.text((275, 35), f"{special_value_username}", fill=rank_color, font=ImageFont.truetype("mine.ttf", 40))
      username_position = (100, 40)
  elif rank_display_name == "Titan":
      rank_color = rank_titan
      draw.text((282, 39), f"{special_value_username}", fill=rank_color, font=ImageFont.truetype("mine.ttf", 40))
      username_position = (100, 43)
  elif rank_display_name == "Champion":
      rank_color = "red"
      username_position = (95, 43)
      draw.text((372, 39), f"{special_value_username}", fill=rank_color, font=ImageFont.truetype("mine.ttf", 40))
  else:
      rank_color = "white"  # Default color if rank not specified
      username_position = (75, 43)

  if rank_display_name != "N/A":
      draw.text((username_position), f"{rank_display_name}", fill=rank_color, font=ImageFont.truetype("mc2.otf", 50))
  else:
      print("No rank found")
      draw.text((85, 43), f"No rank", fill="white", font=ImageFont.truetype("mc2.otf", 45))
      draw.text((312, 33), f"{special_value_username}", fill="white", font=ImageFont.truetype("mine.ttf", 40))
 


  if skin_response2.status_code == 200:
      skin_image2 = Image.open(BytesIO(skin_response2.content)).convert('RGBA')
      skin_image = skin_image2.resize((55, 55), resample=Image.LANCZOS)
      result_image.paste(skin_image, (20, 35), skin_image)
      # Save the image locally for inspection
      skin_image2.save("head_image.png")  # Debugging line
  else:
      print("Failed to retrieve head image.")  # Debugging lineZumi

  # Drawing text and statistic

  #draw.text((395, 35), f"{username.replace('_', ' ').capitalize()} ", fill='white', font=ImageFont.truetype("mine.ttf", 40))

  draw.text((1020, 680), f"({mode.replace('_', ' ').lower()}) ({interval.lower().capitalize()})", fill='white', font=ImageFont.truetype("mine.ttf", 20))
  rank_level = additional_data["rank"].get("level", "N/A")

  stat_positions = [
      ("Wins", get_entry_value(pika_data, "Wins"), (105, 190), get_place(pika_data, "Wins")),  # 160
      ("Losses", get_entry_value(pika_data, "Losses"), (338, 190), get_place(pika_data, "Losses")),
      ("Final deaths", get_entry_value(pika_data, "Final deaths"), (336, 310), get_place(pika_data, "Final deaths")),
      ("Final kills", get_entry_value(pika_data, "Final kills"), (105, 310), get_place(pika_data, "Final kills")),
      ("Beds broken", get_entry_value(pika_data, "Beds destroyed"), (100, 558), get_place(pika_data, "Beds destroyed")),  # 85
      ("Beds lost", get_entry_value(pika_data, "Losses"), (332, 558), get_place(pika_data, "Losses")),
      ("Kills", get_entry_value(pika_data, "Kills"), (105, 440), get_place(pika_data, "Kills")),
      ("Deaths", get_entry_value(pika_data, "Deaths"), (335, 440), get_place(pika_data, "Deaths")),
      ("Arrows hit", get_arrow_hit(username, interval, mode), (787, 310), None),  # Adding Arrows Hit
      ("Arrows ratio", get_arrow_ratio(username, interval, mode), (788, 558), None),  # Adding Arrows Ratio
      ("Exploits", get_exploits(username, interval, mode), (795, 190), None),  # Adding Exploits
  ]

  colors = {
      "Wins": "white",
      "Losses": "red",
      "Final deaths": "white",
      "Final kills": "white",
      "Beds broken": "white",
      "Beds lost": "white",
      "Kills": "white",
      "Deaths": "white",
      "Arrows hit": "white",
      "Arrows ratio": "white",
      "Exploits": "white",
  }

  # Assuming draw is the ImageDraw object
  for stat_name, stat_value, position, place in stat_positions:
    draw.text(position, f"{stat_value}", fill=colors[stat_name], anchor="ms", font=ImageFont.truetype("mc.ttf", 30))
    if place is not None:
        draw.text((position[0], position[1] + 20), f"#{place}", fill="white", anchor="ms", font=ImageFont.truetype("mc.ttf", 18))

  highest_winstreak_value = get_entry_value(pika_data, "Highest winstreak reached")
  draw.text((569, 438), f"{highest_winstreak_value}", fill='white', anchor="ms", font=ImageFont.truetype("mc.ttf", 30))

  # Api section

  # Kill-to-death ratio
  kills = int(get_entry_value(pika_data, "Kills"))
  deaths = int(get_entry_value(pika_data, "Deaths"))
  kill_to_death_ratio = kills / deaths if deaths > 0 else kills

  if kill_to_death_ratio > 5:
      color_kdr = 'green'
  elif kill_to_death_ratio > 1:
      color_kdr = 'yellow'
  else:
      color_kdr = 'red'

  draw.text((792, 438), f"{kill_to_death_ratio:.2f}", fill=color_kdr, anchor="ms", font=ImageFont.truetype("mc.ttf", 30))

  final_deaths = int(get_entry_value(pika_data, "Final deaths"))
  final_kills = int(get_entry_value(pika_data, "Final kills"))
  final_kill_to_death_ratio = final_kills / final_deaths if final_deaths > 0 else final_kills

  if final_kill_to_death_ratio > 5:
      color_final_kdr = 'green'
  elif final_kill_to_death_ratio > 1:
      color_final_kdr = 'yellow'
  else:
      color_final_kdr = 'red'

  draw.text((565, 310), f"{final_kill_to_death_ratio:.2f}", fill=color_final_kdr, anchor="ms", font=ImageFont.truetype("mc.ttf", 30))

  wins = int(get_entry_value(pika_data, "Wins"))
  losses = int(get_entry_value(pika_data, "Losses"))
  win_to_loss_ratio = wins / losses if losses > 0 else wins

  if win_to_loss_ratio > 5:
      color_win_to_loss = 'green'
  elif win_to_loss_ratio > 1:
      color_win_to_loss = 'yellow'
  else:
      color_win_to_loss = 'red'

  draw.text((570, 190), f"{win_to_loss_ratio:.2f}", fill=color_win_to_loss, anchor="ms", font=ImageFont.truetype("mc.ttf", 30))

  last_seen_string = get_last_seen(username)

  # Create an image with Pillow
  
  
  font = ImageFont.truetype("mc2.otf", 20)
  draw.text((955, 450), f"Last Seen: {last_seen_string}", fill="white", font=font)

  games_played = get_entry_value(pika_data, "Games played")
  draw.text((558, 558), f"{games_played}", fill='white', anchor="ms", font=ImageFont.truetype("mc.ttf", 30))
  draw.text((1075, 515), f"Guild", fill='white', anchor="ms", font=ImageFont.truetype("mc1.otf", 50))

  if additional_data.get("clan"):
      clan_name = additional_data["clan"].get("name", "No Clan")
      draw.text((1075, 545), f"{clan_name}", fill='white', anchor="ms", font=ImageFont.truetype("mc1.otf", 30))
      guild_owner, guild_level, guild_members = get_guild_info(username)
      draw.text((1075, 570), f"Owner-{guild_owner}", fill='white', anchor="ms", font=ImageFont.truetype("mc.ttf", 26))
      draw.text((1075, 600), f"Level:{guild_level}", fill='white', anchor="ms", font=ImageFont.truetype("mc.ttf", 26))
      draw.text((1075, 625), f"Members:{guild_members}", fill='white', anchor="ms", font=ImageFont.truetype("mc.ttf", 26))
      
  else:
      draw.text((1065, 545), f"No Guild", fill='white', anchor="ms", font=ImageFont.truetype("mc1.otf", 26))

  if additional_data.get("rank"):  # Checking if "rank" key exists in additional_data
      rank_level = additional_data["rank"].get("level", "N/A")  # Extracting "level" value, defaulting to "N/A" if not found

      # Setting color based on rank level
      if rank_level is not None:
          if rank_level >= 100:
              level_color = 'red'
          elif rank_level >= 75:
              level_color = 'yellow'
          elif rank_level >= 60:
              level_color = 'orange'
          elif rank_level >= 50:
              level_color = 'pink'
          elif rank_level >= 45:
              level_color = 'aqua'
          elif rank_level >= 40:
              level_color = 'dark_green'
          elif rank_level >= 35:
              level_color = 'white'
          elif rank_level >= 30:
              level_color = 'red'
          elif rank_level >= 25:
              level_color = 'yellow'
          elif rank_level >= 20:
              level_color = 'orange'
          elif rank_level >= 15:
              level_color = 'pink'
          elif rank_level >= 10:
              level_color = 'aqua'
          elif rank_level >= 5:
              level_color = 'light_green'
          elif rank_level >= 1:
              level_color = 'white'
          else:
              level_color = 'white'  

      else:
          rank_level = "N/A"
          level_color = 'red'  # Default color if level is not found

      draw.text((1045, 115), f"{rank_level}", fill=level_color, font=ImageFont.truetype("mc2.otf", 46))  # Displaying the level with the determined color
  else:
      draw.text((1043, 115), "0", fill='red', font=ImageFont.truetype("mc2.otf", 46))  # If "rank" key not found, display "No Levels Found!"

  return result_image

def get_entry_value(data, key):
  entry_data = data.get(key, {}).get('entries', None)
  if entry_data is not None:
      return entry_data[0].get('value', 'N/A')
  else:
      return 0

def get_place(data, key):
  entry_data = data.get(key, {}).get('entries', None)
  if entry_data is not None:
      return entry_data[0].get('place', None)
  else:
      return None




def crop_to_circle(image):
  size = min(image.size)
  mask = Image.new("L", (size, size), 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0, size, size), fill=255)
  output = Image.new("RGBA", (size, size))
  output.paste(image, (int((size - image.size[0]) / 2), int((size - image.size[1]) / 2)))
  output.putalpha(mask)
  return output



@app.route('/wel/<name>/<slogan>')
def generate_welcome_image(name, slogan):
  try:
      # Load custom background image
      background_path = "custom_background.png"
      background = Image.open(background_path)
      width, height = background.size

      # Get avatar link from query parameters
      avatar_link = request.args.get('pfp')

      # Load and resize avatar image from link
      avatar_size = (120, 120)
      response = requests.get(avatar_link)
      avatar_img = Image.open(BytesIO(response.content))
      avatar_img = avatar_img.resize(avatar_size)

      # Crop avatar image to circle
      avatar_img = crop_to_circle(avatar_img)

      # Add avatar image to background
      background.paste(avatar_img, (20, 40), avatar_img)

      # Add name text to background
      draw = ImageDraw.Draw(background)
      font = ImageFont.truetype("arial.ttf", 30)
      draw.text((230, 60), f"Welcome, {name}!", fill="white", font=font)

      # Add slogan text to background
      draw.text((230, 100), slogan, fill="white", font=font)

      # Save image
      img_path = 'welcome_image.png'
      background.save(img_path)

      return send_file(img_path, mimetype='image/png')

  except Exception as e:
      error_message = f"Apologies, but an error occurred: {str(e)}"
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=35819, debug=True)

