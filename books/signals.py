import os
from .models import Book
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, post_init


@receiver(post_save, sender=Book)
def Book_pos_save(sender, instance, created, **kwargs):
    """
    A signal handler function for renaming cover with same identifier as the title
    """
    if not hasattr(instance, '_performing_post_save'):
        instance._performing_post_save = False

    if not instance._performing_post_save:
        instance._performing_post_save = True

        if created or instance.cover_image != instance._original_cover_image:
            if instance.cover_image:
                cover_name = f"{instance.url_title}_cover.jpg"
                current_cover_path = instance.cover_image.path
                new_cover_path = os.path.join(os.path.dirname(current_cover_path), cover_name)
                os.rename(current_cover_path, new_cover_path)
                instance.cover_image.name = os.path.relpath(new_cover_path, 'media')
                instance.save(update_fields=['cover_image'])

        instance._performing_post_save = False


@receiver(pre_save, sender=Book)
def update_cover(sender, instance, **kwargs):
    """
    A signal handler function for checking pre save if cover exists and deletes old file if changed
    """
    print("Entering pre_save signal")
    if instance.pk:
        try:
            old_instance = Book.objects.get(pk=instance.pk)
            if old_instance.cover_image != instance.cover_image:
                if old_instance.cover_image:
                    if os.path.exists(old_instance.cover_image.path):
                        os.remove(old_instance.cover_image.path)
        except Book.DoesNotExist:
            pass


@receiver(post_init, sender=Book)
def store_original_cover(sender, instance, **kwargs):
    """
    A signal handler function for creating copy of the cover_image to check whether updated later on
    """
    instance._original_cover_image = instance.cover_image


@receiver(post_delete, sender=Book)
def delete_cover_image(sender, instance, **kwargs):
    """
    A signal handler function for deleting cover file from filesystem
    when corresponing 'Book' onject is deleted
    """
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)
