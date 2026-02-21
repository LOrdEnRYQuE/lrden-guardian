#!/usr/bin/env python3
"""
LRDEnE Guardian Discord Integration
===================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Real-time AI safety monitoring for Discord messages and content.
"""

import os
import json
import logging
import asyncio
import datetime
from typing import Dict, List, Any, Optional

import discord
from discord.ext import commands
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LRDEnEGuardianDiscord:
    """LRDEnE Guardian Discord Bot"""
    
    def __init__(self):
        self.api_endpoint = os.getenv('LRDEN_GUARDIAN_API_ENDPOINT', 'http://localhost:5001')
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        
        if not self.discord_token:
            raise ValueError("DISCORD_BOT_TOKEN environment variable is required")
        
        # Initialize Discord bot
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        self.bot = commands.Bot(
            command_prefix='/guardian ',
            intents=intents,
            help_command=None
        )
        
        # Analysis cache
        self.analysis_cache = {}
        
        # Setup bot handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup Discord event handlers"""
        
        @self.bot.event
        async def on_ready():
            """Bot ready event"""
            logger.info(f"LRDEnE Guardian Discord bot is ready! Logged in as {self.bot.user}")
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="for AI safety risks 🛡️"
                )
            )
        
        @self.bot.event
        async def on_message(message):
            """Handle incoming messages"""
            try:
                # Skip bot messages
                if message.author.bot:
                    return
                
                # Skip very short messages
                content = message.content.strip()
                if len(content) < 10:
                    return
                
                # Analyze the message
                analysis = await self.analyze_content(content, {
                    'source': 'discord_integration',
                    'author_id': str(message.author.id),
                    'author_name': str(message.author),
                    'channel_id': str(message.channel.id),
                    'channel_name': message.channel.name,
                    'guild_id': str(message.guild.id) if message.guild else None,
                    'guild_name': message.guild.name if message.guild else None,
                    'message_type': 'message',
                    'timestamp': message.created_at.isoformat()
                })
                
                if analysis and not analysis.get('is_safe', True):
                    await self.handle_risky_content(analysis, message)
                    
            except Exception as e:
                logger.error(f"Error handling message: {e}")
        
        @self.bot.command(name='analyze')
        async def analyze_command(ctx, *, text: str = None):
            """Manually analyze text"""
            try:
                if not text:
                    await ctx.send("Please provide text to analyze. Usage: `/guardian analyze <text>`")
                    return
                
                await ctx.trigger_typing()
                
                analysis = await self.analyze_content(text, {
                    'source': 'discord_command',
                    'author_id': str(ctx.author.id),
                    'author_name': str(ctx.author),
                    'channel_id': str(ctx.channel.id),
                    'command': True
                })
                
                if analysis:
                    await self.send_analysis_embed(analysis, ctx)
                else:
                    await ctx.send("❌ Analysis failed. Please try again later.")
                    
            except Exception as e:
                logger.error(f"Error in analyze command: {e}")
                await ctx.send("❌ An error occurred during analysis.")
        
        @self.bot.command(name='status')
        async def status_command(ctx):
            """Check Guardian status"""
            try:
                status = await self.check_guardian_status()
                if status:
                    embed = discord.Embed(
                        title="🛡️ LRDEnE Guardian Status",
                        description="✅ **Online**",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="API Endpoint", value=f"`{self.api_endpoint}`", inline=False)
                    embed.add_field(name="Bot Version", value="1.0.0", inline=True)
                    embed.add_field(name="Cache Size", value=str(len(self.analysis_cache)), inline=True)
                else:
                    embed = discord.Embed(
                        title="🛡️ LRDEnE Guardian Status",
                        description="❌ **Offline**",
                        color=discord.Color.red()
                    )
                    embed.add_field(name="API Endpoint", value=f"`{self.api_endpoint}`", inline=False)
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                logger.error(f"Error in status command: {e}")
                await ctx.send("❌ Unable to check status.")
        
        @self.bot.command(name='settings')
        async def settings_command(ctx):
            """Show current settings"""
            try:
                embed = discord.Embed(
                    title="🛡️ LRDEnE Guardian Settings",
                    color=discord.Color.blue()
                )
                embed.add_field(name="🔗 API Endpoint", value=f"`{self.api_endpoint}`", inline=False)
                embed.add_field(name="📊 Auto-analysis", value="✅ Enabled", inline=True)
                embed.add_field(name="⚠️ Risk Alerts", value="✅ Enabled", inline=True)
                embed.add_field(name="📈 Statistics", value="✅ Enabled", inline=True)
                
                embed.set_footer(text="Use `/guardian analyze <text>` to manually analyze content")
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                logger.error(f"Error in settings command: {e}")
                await ctx.send("❌ Unable to retrieve settings.")
        
        @self.bot.command(name='help')
        async def help_command(ctx):
            """Show help information"""
            embed = discord.Embed(
                title="🛡️ LRDEnE Guardian Help",
                description="AI Safety and Hallucination Detection for Discord",
                color=discord.Color.purple()
            )
            
            commands = [
                ("/guardian analyze <text>", "Manually analyze text content"),
                ("/guardian status", "Check Guardian API status"),
                ("/guardian settings", "View current settings"),
                ("/guardian help", "Show this help message")
            ]
            
            for cmd, desc in commands:
                embed.add_field(name=cmd, value=desc, inline=False)
            
            embed.add_field(
                name="🔧 Features",
                value="• Real-time message analysis\n• Risk detection and alerts\n• Guardian scoring system\n• Detailed analysis reports",
                inline=False
            )
            
            embed.set_footer(text="LRDEnE Guardian - Your AI Safety Partner")
            
            await ctx.send(embed=embed)
    
    async def analyze_content(self, content: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze content using LRDEnE Guardian API"""
        try:
            # Check cache first
            cache_key = hash(content + str(context))
            if cache_key in self.analysis_cache:
                return self.analysis_cache[cache_key]
            
            # Call LRDEnE Guardian API
            response = requests.post(
                f"{self.api_endpoint}/analyze",
                json={
                    "content": content,
                    "context": {
                        **context,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                analysis = response.json()
                
                # Cache the result
                self.analysis_cache[cache_key] = analysis
                
                # Limit cache size
                if len(self.analysis_cache) > 1000:
                    oldest_key = next(iter(self.analysis_cache))
                    del self.analysis_cache[oldest_key]
                
                return analysis
            else:
                logger.error(f"API request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing content: {e}")
            return None
    
    async def handle_risky_content(self, analysis: Dict[str, Any], message: discord.Message):
        """Handle risky content detection"""
        try:
            # Don't alert in public channels to avoid embarrassment
            if not message.channel.permissions_for(message.guild.me).send_messages:
                return
            
            # Create warning embed
            risk_level = analysis.get('risk_level', 'unknown')
            guardian_score = analysis.get('guardian_score', 0)
            issues = analysis.get('detected_issues', [])
            
            # Choose color based on risk level
            colors = {
                'low': discord.Color.orange(),
                'medium': discord.Color.red(),
                'high': discord.Color.dark_red(),
                'critical': discord.Color.purple()
            }
            color = colors.get(risk_level, discord.Color.red())
            
            embed = discord.Embed(
                title="🛡️ LRDEnE Guardian Alert",
                description=f"⚠️ **Risk Level: {risk_level.upper()}**\n📊 **Guardian Score: {guardian_score:.3f}**",
                color=color
            )
            
            # Add issues if any (limit to avoid too long messages)
            if issues:
                issues_text = "\n".join([f"• {issue}" for issue in issues[:3]])
                embed.add_field(name="🚨 Detected Issues", value=issues_text, inline=False)
            
            # Add footer with context
            embed.set_footer(text=f"Message from {message.author.name} in #{message.channel.name}")
            
            # Send as ephemeral message if possible, otherwise send warning
            try:
                # Try to send DM to the user
                await message.author.send(embed=embed)
            except discord.Forbidden:
                # If DM is not possible, send a subtle warning in the channel
                await message.add_reaction("⚠️")
                await message.channel.send(
                    f"🛡️ LRDEnE Guardian detected potential issues in a recent message. "
                    f"Please review content carefully. (Risk Level: {risk_level.upper()})",
                    delete_after=30  # Auto-delete after 30 seconds
                )
            
        except Exception as e:
            logger.error(f"Error handling risky content: {e}")
    
    async def send_analysis_embed(self, analysis: Dict[str, Any], ctx):
        """Send analysis results as Discord embed"""
        try:
            is_safe = analysis.get('is_safe', True)
            risk_level = analysis.get('risk_level', 'unknown')
            guardian_score = analysis.get('guardian_score', 0)
            confidence = analysis.get('confidence_score', 0)
            issues = analysis.get('detected_issues', [])
            recommendations = analysis.get('recommendations', [])
            
            # Choose color based on safety
            if is_safe:
                color = discord.Color.green()
                status_icon = "✅"
                status_text = "Safe Content"
            else:
                colors = {
                    'low': discord.Color.orange(),
                    'medium': discord.Color.red(),
                    'high': discord.Color.dark_red(),
                    'critical': discord.Color.purple()
                }
                color = colors.get(risk_level, discord.Color.red())
                status_icon = "⚠️"
                status_text = "Requires Review"
            
            embed = discord.Embed(
                title="🛡️ LRDEnE Guardian Analysis",
                description=f"{status_icon} **Status: {status_text}**",
                color=color
            )
            
            embed.add_field(name="📊 Guardian Score", value=f"{guardian_score:.3f}", inline=True)
            embed.add_field(name="🎯 Confidence", value=f"{confidence:.1%}", inline=True)
            embed.add_field(name="🔥 Risk Level", value=risk_level.upper(), inline=True)
            
            # Add issues if any
            if issues:
                issues_text = "\n".join([f"• {issue}" for issue in issues[:3]])
                embed.add_field(name="🚨 Detected Issues", value=issues_text, inline=False)
            
            # Add recommendations if any
            if recommendations:
                rec_text = "\n".join([f"• {rec}" for rec in recommendations[:3]])
                embed.add_field(name="💡 Recommendations", value=rec_text, inline=False)
            
            embed.set_footer(text=f"Analysis requested by {ctx.author.name}")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error sending analysis embed: {e}")
            await ctx.send("❌ Error sending analysis results.")
    
    async def check_guardian_status(self) -> bool:
        """Check if LRDEnE Guardian API is accessible"""
        try:
            response = requests.get(f"{self.api_endpoint}/api-info", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    async def start(self):
        """Start the Discord bot"""
        try:
            # Check Guardian API status
            if not await self.check_guardian_status():
                logger.warning("LRDEnE Guardian API is not accessible")
            
            # Start the bot
            await self.bot.start(self.discord_token)
            
        except Exception as e:
            logger.error(f"Error starting Discord bot: {e}")
            raise

def main():
    """Main entry point"""
    try:
        bot = LRDEnEGuardianDiscord()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Shutting down LRDEnE Guardian Discord bot...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
