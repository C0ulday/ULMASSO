from Intranet.models import Notification

def notifications(request):
    """Injecte les notifications non lues dans tous les templates intranet."""
    if 'loggedMemberId' not in request.session:
        return {}
    from Intranet.models import Member
    try:
        member = Member.objects.get(id=request.session['loggedMemberId'])
        notifs = Notification.objects.filter(recipient=member).order_by('-created_at')[:8]
        unread = Notification.objects.filter(recipient=member, is_read=False).count()
        return {
            'notifications': notifs,
            'notif_count':   unread,
        }
    except Exception:
        return {}
