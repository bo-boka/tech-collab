
from django.contrib.auth.models import User
from collab.models import Project, Match
from taggit.models import Tag


def generate_matches(form):
    """
    Gets project skills and city, finds users with those skills that live in the same city
    and creates Match object with a rank of how many skills the user matched to the project.
    :param form: project model form
    :return: None
    """
    # grabs project skills & city
    p_skills = Tag.objects.filter(project__id=form.instance.id)
    p_city = Project.objects.filter(id=form.instance.id).values('city')[0]['city']

    # grabs users by matching skills and location, excludes project creator
    user_list = User.objects.filter(userprofile__skills__in=p_skills
                                    ).filter(userprofile__city=p_city
                                             ).exclude(id=form.instance.founder.id)

    # todo if userlist is empty, find all matches with project if any exist,
    #  delete from db, & return

    # puts users in dict by their frequency (# matched skills) in queryset
    dict = {}
    for u in user_list:
        if u not in dict:
            dict[u] = 1
        else:
            dict[u] += 1

    # converts user into match obj with frequency as rank
    for key, value in dict.items():
        lookup = {'user': key, 'project': form.instance}
        defaults = {'rank': value}
        match = create_or_update_match(lookup, defaults)

        # match = Match(user=key, project=form.instance, rank=value)
        match.save()


def create_or_update_match(lookup, defaults):

    # todo if defaults rank is 0, throw error

    try:
        instance = Match.objects.get(**lookup)
    except Match.DoesNotExist:
        instance = Match.objects.create(**lookup, **defaults)
        print("New Match created: {}\n".format(instance.id))
        return instance
    else:
        for key, value in defaults.items():
            attr = getattr(instance, key)
            if attr != value:
                Match.objects.filter(**lookup).update(**defaults)
                # instance.update(**defaults)
                instance.refresh_from_db()
                print("Match updated: {}".format(instance.id))
                return instance
        return instance
