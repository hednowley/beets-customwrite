from beets.plugins import BeetsPlugin
from beets import mediafile


class CustomWrite(BeetsPlugin):
    def __init__(self):
        super(CustomWrite, self).__init__()
        self.register_listener('write', self.loaded)
        self.register_listener('import_task_apply', self.choice)
        field = mediafile.MediaField(
            mediafile.MP3DescStorageStyle(u'customwrite'),
            mediafile.StorageStyle(u'customwrite')
        )
        self.add_media_field('customwrite', field)

    def choice(self, session, task):
        # import pudb; pu.db
        flag = None
        while flag is None:
            user_input = raw_input("Do you want to use customwrite? (y/n) ")
            cleaned_input = user_input.strip().lower()
            if cleaned_input == 'y':
                flag = '1'
            elif cleaned_input == 'n':
                flag = '0'
            else:
                print("Please enter 'y' or 'n'.")

        for i in task.items:
            i.customwrite = flag

    def loaded(self, path, item, tags):
        # import pdb; pdb.set_trace()
        # print dict(item)
        # import pudb; pu.db

        if hasattr(item, "customwrite") and (item.customwrite == '1' \
        or item.customwrite == 1 or item.customwrite is True):
            # print 'customwrite ON!'
            if dict(item)['data_source'] == 'Discogs':
                temp_tag = tags['year']
                tags['year'] = tags['original_year']
                tags['original_year'] = temp_tag
                # print 'discogs'
            label_tag = tags['label']
            if label_tag != '':
                label_tag = ', ' + label_tag
            tags['album'] = tags['album'] + \
                ' (' + tags['media'] + ', ' + \
                str(tags['year']) + label_tag + ')'
            tags['year'] = tags['original_year']
        # else:
            # print 'customwrite OFF!'
